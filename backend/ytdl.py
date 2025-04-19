import os
import subprocess


def download_yt_vid(url: str, output_path: str) -> str:
    result = subprocess.run(
        ["yt-dlp", "--print", "after_move:filepath", "-o", output_path, url],
        capture_output=True,
    )
    if result.returncode != 0:
        print("Error occurred while running `yt-dlp`")
        exit(1)
    else:
        return result.stdout.strip().decode()
