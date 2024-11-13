# ThreatWatch: Real-time DDoS Detection and Network Monitoring Application

**ThreatWatch** is a real-time DDoS detection and network monitoring application. Users can register and manage their client machines through lightweight agents that provide real-time **network analytics, ML-based threat detection, and DDoS attack simulation**—all controlled via a central dashboard.

## Features

- **Real-time DDoS Detection**: Uses machine learning models to detect and visualize DDoS attacks.
- **Network Analytics**: Delivers real-time network insights and metrics for all connected client machines.
- **Client Agent Management**: Users install agents on client machines for monitoring, which persistently connect to the ThreatWatch server.
- **DDoS Attack Simulation**: Configure and launch simulated DDoS attacks on registered clients to stress-test network resilience.
- **Remote Control and Settings**: Control agent behavior remotely, start/stop agents, and update settings directly from the ThreatWatch dashboard.
- **Persistent Connections**: The client agent reconnects automatically after a reboot, ensuring continuous monitoring.

## Table of Contents

- [Installation](#installation)
- [Agent Installation](#agent-installation)
- [Usage](#usage)
  - [Server Setup](#server-setup)
  - [Dashboard](#dashboard)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)
- [License](#license)

## Installation

### Prerequisites

1. **Python 3.8+** for both server and agent.
2. **Redis** for managing WebSocket connections.
3. **Flask-SocketIO** for real-time communication.
4. **psutil** for network data gathering.
5. **Node.js** (optional) for an advanced frontend.

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/threatwatch.git
   cd threatwatch
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Redis (installation steps depend on your OS).

## Agent Installation

The ThreatWatch client agent should be installed on each machine you want to monitor.

1. Copy `agent.py` to the target machine.
2. Install dependencies:
   ```bash
   pip install websockets psutil
   ```
3. Update `agent.py` with your server’s URL and API key:
   ```python
   SERVER_URL = "ws://your-server-url.com:5000/ws"
   API_KEY = "your-unique-user-api-key"
   ```
4. Run the agent:
   ```bash
   python agent.py
   ```

5. (Optional) Set up the agent as a background service for persistence across reboots. (Refer to **Persistent Background Service Setup** below.)

## Usage

### Server Setup

1. Start Redis.
2. Launch the ThreatWatch server:
   ```bash
   python app.py
   ```

3. If needed, run the WebSocket server as a separate process:
   ```bash
   python websocket_server.py
   ```

### Dashboard

The ThreatWatch dashboard enables users to:

- View real-time network traffic data.
- Monitor network insights and ML analytics.
- Simulate DDoS attacks.
- Control agent settings remotely and view agent status.

Access the dashboard at `http://localhost:5000` (or your deployed server URL).

## Project Structure

```plaintext
├── agent.py               # Client-side monitoring agent
├── app.py                 # Main application server
├── websocket_server.py    # WebSocket server for persistent connections
├── static/                # Frontend files (React/HTML/CSS)
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```

## Future Improvements

- **Expanded ML Analytics**: Additional models for anomaly detection.
- **Role-based Access Control**: Permissions based on user roles.
- **Agent Auto-Update**: Enable server-triggered updates for the agent.
- **Enhanced Visualization**: More interactive and detailed charts for network data.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
