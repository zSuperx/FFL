import asyncio
import json
from typing import Callable
import re
import os

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, WebSocketException

import backend.video_utils as video_utils
import backend.parse_frames as parse_frames

app = FastAPI()

# A dictionary to hold event handlers
event_handlers = {}

# Youtube URL regex
regex = re.compile(r"https://youtube\.com/watch.+")


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
        except WebSocketDisconnect:
            print("Connection closed by some client.")
        except Exception as e:
            await websocket.send_text(f"Error: {str(e)}")


@on_event("process-video")
async def event_process_video(websocket: WebSocket, data: dict):
    url = data["data"].get("url")
    video_type = data["data"].get("type")

    print(f"Received request!")
    print(f"{video_type = }, {url = }")

    h = hash(url)

    directory = os.path.join("videos", str(h))
    os.makedirs(directory, exist_ok=True)
    video_path = os.path.join(directory, "video")

    try:

        downloaded_video = video_utils.download_yt_vid(
            url,
            video_path,
        )

        if downloaded_video is None:
            await websocket.send_text("An error occurred while downloading the video")
            return

        print(f"Finished downloading video")

        if (
            video_utils.scale_video(
                downloaded_video, os.path.relpath(downloaded_video), 1000
            )
            != 0
        ):
            await websocket.send_text("An error occurred while scaling the video")
            return

        frames_dir = os.path.dirname(downloaded_video)

        if video_utils.extract_frames(frames_dir, downloaded_video, 4) != 0:
            await websocket.send_text(
                "An error occurred while extracting frames from the video"
            )
            return

        print(f"Finished extracting frames")

        generator = parse_frames.compare_frames(frames_dir, 4)

        for chunk in generator:
            print(chunk)
            await websocket.send_text(f"{chunk = }")

        await websocket.send_text(f"Done")
    finally:
        os.rmdir(directory)
