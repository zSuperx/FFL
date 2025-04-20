import os
import subprocess

from ffmpeg import FFmpeg


def scale_video(url, outputFile, area=10000):
    # -vf scale=2*floor(sqrt(1000*iw/ih)/2):2*floor(1000/sqrt(1000*iw/ih)/2),setsar=1:1
    widthEq = f"'2*floor(min(iw,sqrt({area}*iw/ih))/2)'"
    heightEq = f"'2*floor(min(ih,{area}/sqrt({area}*iw/ih))/2)'"
    vf = f"scale={widthEq}:{heightEq},setsar=1:1"
    print(vf)
    ffmpeg = FFmpeg().option("i", url).option("vf", vf).option("y").output(outputFile)

    ffmpeg.execute()


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
