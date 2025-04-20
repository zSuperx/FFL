from fastapi import FastAPI, WebSocket
from typing import Callable
import json

app = FastAPI()

# A dictionary to hold event handlers
event_handlers = {}


# Function to register event handlers
def on_event(event: str):
    def decorator(func: Callable):
        event_handlers[event] = func
        return func

    return decorator


# Default WebSocket handler
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Receive message (expects JSON with "event" and "data")
        msg = await websocket.receive_text()
        try:
            data = json.loads(msg)
            event = data.get("event")
            if event in event_handlers:
                # Call the corresponding handler
                await event_handlers[event](websocket, data)
            else:
                await websocket.send_text(f"Unknown event: {event}")
        except json.JSONDecodeError:
            await websocket.send_text("Invalid JSON")
        except Exception as e:
            await websocket.send_text(f"Error: {str(e)}")


# Event handler for the "echo" event
@on_event("process-video")
async def handle_echo(websocket: WebSocket, data: dict):
    print(f"{data = }")
    await websocket.send_text(f"Shut up loser")
