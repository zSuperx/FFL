import os
from ytdl import download_yt_vid
from mp4dl import scale_video
from app import app, socketio

URL = "https://www.youtube.com/watch?v=6yrdS4tIP9U"
# URL = "https://www.youtube.com/watch?v=uHU4_Wo4_OY"


def main():
    print("Hello from ffl!")
    socketio.run(app, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
