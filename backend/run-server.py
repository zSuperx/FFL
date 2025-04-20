import asyncio
import json
from typing import Callable

from fastapi import FastAPI, WebSocket

from backend.process_video import process_video

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
                asyncio.create_task(event_handlers[event](websocket, data))
            else:
                await websocket.send_text(f"Unknown event: {event}")
        except json.JSONDecodeError:
            await websocket.send_text("Invalid JSON")
        except Exception as e:
            await websocket.send_text(f"Error: {str(e)}")


@on_event("process-video")
async def event_process_video(websocket: WebSocket, data: dict):
    url = data["data"].get("url")
    video_type = data["data"].get("type")

    print(f"{video_type = }, {url = }")
    generator = process_video(url, video_type)

    for chunk in generator:
        await websocket.send_text(f"Processed some more shit, but then again maybe not")

    await websocket.send_text(f"Done")
