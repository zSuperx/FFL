import os
import subprocess


def download_yt_vid(url: str, output_path: str):
    result = subprocess.run(["yt-dlp", url, "-o", output_path])
    if result.returncode != 0:
        print("Error occurred while running `yt-dlp`")
        exit(1)
