from process_video import process_video
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("start-processing")
def process(data):
    print(f"Received request: {data}")

    url = data["url"]
    video_type = data["type"]

    print(url)
    print(video_type)

    for _ in range(10):
        emit(
            "time-slice",
            {
                "start": 42,
                "duration": 5,
            },
        )

    res = process_video(url, video_type)

    return res
