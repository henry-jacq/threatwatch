import asyncio
import websockets
import psutil
import json
import socket
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Setup constants
load_dotenv()
SERVER_URL = os.getenv("SERVER_URL")
API_KEY = os.getenv("API_KEY")
MACHINE_ID = os.getenv("MACHINE_ID")

# Configure logging
LOG_FILE = Path("agent.log")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format="%(asctime)s %(levelname)s: %(message)s")


async def get_network_metrics():
    """Collects network metrics using psutil library."""
    stats = psutil.net_io_counters()
    return {
        "bytes_sent": stats.bytes_sent,
        "bytes_recv": stats.bytes_recv,
        "packets_sent": stats.packets_sent,
        "packets_recv": stats.packets_recv
    }


async def connect_to_server():
    """Establishes WebSocket connection and sends periodic data to the server."""
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    async with websockets.connect(SERVER_URL) as websocket:
        # Send initial connection message
        connect_message = json.dumps({
            "type": "connect",
            "api_key": API_KEY,
            "machine_id": MACHINE_ID,  # Send machine_id for identification
            "hostname": hostname,
            "ip": ip_address
        })
        await websocket.send(connect_message)
        logging.info(f"Connected to server with Machine ID: {MACHINE_ID}.")

        # Main data sending loop
        while True:
            # Gather and send network metrics
            data = await get_network_metrics()
            message = json.dumps(
                {"type": "data", "api_key": API_KEY, "machine_id": MACHINE_ID, "data": data})
            await websocket.send(message)
            logging.info(f"Data sent from Machine ID: {MACHINE_ID}.")

            # Wait for server commands or control messages
            try:
                server_response = await websocket.recv()
                response = json.loads(server_response)

                if response.get("command") == "stop":
                    logging.info(
                        f"Received stop command from server. Disconnecting Machine ID: {MACHINE_ID}...")
                    break  # Stop the agent
                elif response.get("command") == "update":
                    logging.info(
                        f"Received update command from server for Machine ID: {MACHINE_ID}.")
                    # Logic for updating agent here (e.g., reloading settings or downloading updates)

            except websockets.ConnectionClosed as e:
                logging.error(f"Connection lost: {
                              e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)
                break

    # Reconnect logic
    await asyncio.sleep(5)
    await connect_to_server()


async def main():
    """Continuously attempts to connect to the server."""
    while True:
        try:
            await connect_to_server()
        except Exception as e:
            logging.error(f"Connection error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
