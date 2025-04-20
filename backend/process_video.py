import os
import time

from mp4dl import scale_video
from ytdl import download_yt_vid
from extract_frames import extract_frames


def get_directory(url):
    ms = int(round(time.time() * 1000))
    h = hash(url)

    directory = f"videos/{ms}_{h}/"
    os.makedirs(directory, exist_ok=True)
    return directory


def process_video(url: str, video_type: str):
    # How risky is this video?
    severity = 0
    # List of 2-length lists: range where flashing lights occur
    timestamps = []

    directory = get_directory(url)
    videoName = directory + "video.mp4"

    if video_type == "youtube":
        download_yt_vid(url, videoName)
    elif video_type == "video":
        scale_video(url, videoName)

    res = {"severity": severity, "timestamps": timestamps}
    return res
