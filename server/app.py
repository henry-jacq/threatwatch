from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import logging

app = Flask(__name__)
socketio = SocketIO(app)

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s: %(message)s")

@app.route('/')
def index():
    """Renders the index page."""
    return render_template('pages/dashboard.html')


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, use_reloader=True)
