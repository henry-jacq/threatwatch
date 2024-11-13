from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
import json

app = Flask(__name__)
socketio = SocketIO(app)

clients = {}  # Active WebSocket clients by session ID
users_db = {  # Mocked database of users
    "40ba8ded24804d158cbbffdc1088e954": {
        "api_key": "api-key-7890abcdef",
        "ip": "127.0.0.1"
    },
    "unique-machine-id-456": {
        "api_key": "another-api-key",
        "ip": "192.168.1.3"
    }
}

@app.route('/', methods=['GET'])
def index():
    # Displays
    # Active clients, their ip, machine_id, api-key
    return render_template('index.html')

@app.route('/api/agent/connect', methods=['POST'])
def connect_agent():
    data = request.json
    api_key = data.get("api_key")
    machine_id = data.get("machine_id")
    ip = data.get("ip")

    # Validate the machine_id and api_key
    if validate_agent(api_key, machine_id):
        print(f"Agent connected: ({ip}) with ID: {machine_id}")
        return jsonify({"message": "Connected successfully"}), 200
    else:
        return jsonify({"error": "Invalid API key or Machine ID"}), 403


@app.route('/api/agent/data', methods=['POST'])
def receive_data():
    data = request.json
    api_key = data.get("api_key")
    machine_id = data.get("machine_id")

    if not validate_agent(api_key, machine_id):
        return jsonify({"error": "Unauthorized"}), 403

    network_data = data.get("data")
    print(f"Data received from {machine_id}: {network_data}")
    # Optionally store network data in a database

    return jsonify({"message": "Data received successfully."}), 200


@app.route('/api/agent/command', methods=['POST'])
def send_command():
    data = request.json
    machine_id = data.get("machine_id")
    command = data.get("command")

    # Send a command to the agent
    target_sid = get_client_sid_by_machine_id(machine_id)
    if target_sid:
        socketio.emit("control", {"command": command}, room=target_sid)
        return jsonify({"message": f"Command '{command}' sent to agent {machine_id}."}), 200
    else:
        return jsonify({"error": f"Agent with ID {machine_id} not connected."}), 404


def validate_agent(api_key, machine_id):
    """Checks if the API key and machine ID match the records in users_db"""
    user = users_db.get(machine_id)
    if user and user["api_key"] == api_key:
        return True
    return False


def get_client_sid_by_machine_id(machine_id):
    """Returns the WebSocket session ID based on the machine ID"""
    for sid, client in clients.items():
        if client["machine_id"] == machine_id:
            return sid
    return None


@socketio.on('connect')
def on_connect():
    # Assuming machine_id is passed as a query param
    machine_id = request.args.get('machine_id')
    clients[request.sid] = {"machine_id": machine_id, "sid": request.sid}
    print(f"Client connected: {request.sid} with Machine ID: {machine_id}")


@socketio.on('disconnect')
def on_disconnect():
    if request.sid in clients:
        machine_id = clients[request.sid]["machine_id"]
        del clients[request.sid]
        print(f"Client disconnected: {
              request.sid} with Machine ID: {machine_id}")


@socketio.on('control')
def control_agent(data):
    command = data.get("command")
    target_sid = data.get("client_id")

    if target_sid in clients:
        socketio.emit("control", {"command": command}, room=target_sid)
        print(f"Sent '{command}' command to client {target_sid}")
    else:
        print(f"Client {target_sid} not connected")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
