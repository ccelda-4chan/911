import os
import base64
import json
from flask_socketio import emit, join_room, leave_room
from utils.logger import logger

class RemoteEngine:
    def __init__(self, socketio):
        self.socketio = socketio
        self.clients = {} # sid -> client_info

    def register_handlers(self):
        @self.socketio.on('connect')
        def handle_connect():
            logger.info(f"Client connected: {request.sid}")

        @self.socketio.on('disconnect')
        def handle_disconnect():
            if request.sid in self.clients:
                client = self.clients.pop(request.sid)
                logger.info(f"Client disconnected: {client.get('hostname', request.sid)}")
                self.socketio.emit('client_list', self.get_client_list())

        @self.socketio.on('client_auth')
        def handle_auth(data):
            # Register client info
            self.clients[request.sid] = {
                "sid": request.sid,
                "hostname": data.get("hostname", "Unknown"),
                "ip": request.remote_addr,
                "os": data.get("os", "Unknown"),
                "status": "Online"
            }
            logger.info(f"Client authorized: {self.clients[request.sid]['hostname']}")
            self.socketio.emit('client_list', self.get_client_list())

        @self.socketio.on('screen_frame')
        def handle_frame(data):
            # Forward screen frame to web dashboard (in a specific room for that client)
            # data should contain base64 image
            sid = request.sid
            self.socketio.emit('display_frame', data, room=f"admin_{sid}")

        @self.socketio.on('admin_join')
        def handle_admin_join(data):
            # Admin joins a room to monitor a specific client
            target_sid = data.get('target_sid')
            join_room(f"admin_{target_sid}")
            logger.info(f"Admin joined room for client: {target_sid}")

        @self.socketio.on('admin_input')
        def handle_admin_input(data):
            # Forward admin input (mouse/keyboard) to the client agent
            target_sid = data.get('target_sid')
            self.socketio.emit('remote_command', data, room=target_sid)

        @self.socketio.on('shell_output')
        def handle_shell_output(data):
            # Forward shell output to admin room
            sid = request.sid
            self.socketio.emit('display_shell', data, room=f"admin_{sid}")

    def get_client_list(self):
        return list(self.clients.values())

from flask import request
