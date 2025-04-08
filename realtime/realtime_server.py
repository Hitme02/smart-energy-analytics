# Ensure module import works


import asyncio
import websockets
import json
import random
from datetime import datetime
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# Local import of Dijkstra logic
from optimal_distribution.dijkstra_optimizer import SmartGridGraph



# Function to simulate live energy usage + optimal routing
async def send_data(websocket, path):
    print("🔌 Client connected.")

    num_homes = 10
    grid = SmartGridGraph(num_nodes=10)
    grid.generate_random_edges()

    while True:
        # --- Simulated Energy Data ---
        home_id = f"Home_{random.randint(0, num_homes - 1)}"
        energy_kwh = round(random.uniform(0.5, 10.0), 2)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        energy_data = {
            "type": "energy",
            "home": home_id,
            "energy_kwh": energy_kwh,
            "timestamp": timestamp
        }

        await websocket.send(json.dumps(energy_data))

        # --- Simulated Optimal Routing ---
        source_node = random.choice(grid.nodes)
        distances, previous = grid.dijkstra(source_node)

        routing_data = {
            "type": "routing",
            "source": source_node,
            "paths": []
        }

        for target in grid.nodes:
            if target != source_node:
                path = grid.reconstruct_path(previous, target)
                routing_data["paths"].append({
                    "target": target,
                    "path": path,
                    "cost": distances[target]
                })

        await websocket.send(json.dumps(routing_data))

        await asyncio.sleep(5)  # Send data every 5 seconds


# Run WebSocket server
start_server = websockets.serve(send_data, "localhost", 6789)

print("🚀 WebSocket server running at ws://localhost:6789")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
