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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('password') == config.APP_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        error = 'Invalid Password'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', services=services)

@app.route('/attack', methods=['POST'])
@login_required
def start_attack():
    data = request.json
    phone = data.get('phone', '')
    amount = int(data.get('amount', 5))
    selected_services = data.get('services')

    if not re.match(r'^(09\d{9}|9\d{9}|\+639\d{9})$', phone.replace(' ', '')):
        return jsonify({"success": False, "error": "Invalid phone format"}), 400

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
                    "msg": f"Batch {batch}/{total} completed: {success} OK, {failed} FAIL",
                    "type": "info"
                })

        try:
            loop.run_until_complete(engine.run_attack(
                phone, amount, selected_services, on_progress=progress_callback
            ))
        except Exception as e:
            logger.exception("Background attack failed")
            with attack_state["lock"]:
                attack_state["logs"].append({"msg": f"Critical Error: {str(e)}", "type": "error"})
        finally:
            with attack_state["lock"]:
                attack_state["active"] = False
            loop.close()
            gc.collect() # Aggressive cleanup for low RAM

    thread = threading.Thread(target=run_in_bg)
    thread.start()
    
    return jsonify({"success": True})

@app.route('/status')
@login_required
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
