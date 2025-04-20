import os
from ytdl import download_yt_vid
from mp4dl import scale_video

URL = "https://www.youtube.com/watch?v=6yrdS4tIP9U"
# URL = "https://www.youtube.com/watch?v=uHU4_Wo4_OY"


def main():
    print("Hello from ffl!")

    pathname = os.path.join("videos", "test-video1")

    video_path = download_yt_vid(URL, pathname)

    print(f"{video_path = }")
    video_path = os.path.relpath(video_path)

    download_mp4(f"{video_path}.webm", f"{video_path}-scaled.webm")


if __name__ == "__main__":
    main()
