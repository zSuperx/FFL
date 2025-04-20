import os
from ytdl import download_yt_vid
from mp4dl import download_mp4

# URL = "https://www.youtube.com/watch?v=6yrdS4tIP9U"
# URL = "https://www.youtube.com/watch?v=uHU4_Wo4_OY"
URL = "https://www.youtube.com/watch?v=e-DBVELNb5I&ab_channel=wotaku"


def main():
    print("Hello from ffl!")

    video_path = os.path.join("videos", "test-video1")

    download_yt_vid(URL, video_path)

    download_mp4(f"{video_path}.webm", f"{video_path}-scaled.webm")


if __name__ == "__main__":
    main()
