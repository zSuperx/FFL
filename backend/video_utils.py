import os
import subprocess

from ffmpeg import FFmpeg


def download_yt_vid(url: str, output_path: str) -> str | None:
    """
    Calls `yt-dlp` to download the YouTube video from the given `url`.

    The file will be outputted to `output_path`, if it exists and error if it does not.
    """
    result = subprocess.run(
        ["yt-dlp", "--print", "after_move:filepath", "-o", output_path, url],
        capture_output=True,
    )
    if result.returncode != 0:
        print("Error occurred while running `yt-dlp`")
        return None
    else:
        return result.stdout.strip().decode()


def scale_video(url, output_path, area=10000) -> int:
    """
    Scales a video to the given `area` size, keeping the aspect ratio the same.

    `url` can be a URL to the downloadable mp4 or a local path to a video file.
    """
    # -vf scale=2*floor(sqrt(1000*iw/ih)/2):2*floor(1000/sqrt(1000*iw/ih)/2),setsar=1:1
    widthEq = f"'2*floor(min(iw,sqrt({area}*iw/ih))/2)'"
    heightEq = f"'2*floor(min(ih,{area}/sqrt({area}*iw/ih))/2)'"
    vf = f"scale={widthEq}:{heightEq},setsar=1:1"
    print(vf)
    ffmpeg = FFmpeg().option("i", url).option("vf", vf).option("y").output(output_path)

    try:
        ffmpeg.execute()
        return 0
    except Exception as e:
        print(f"Ran into exception {e}")
        return 1


# download_mp4("https://jasonfeng365.github.io/canis/canis-contests.mp4", 'videos/out.mp4')
# extract_frames("videos/", "out.mp4")
def extract_frames(dir: str, video_path: str, fps: int) -> int:
    """
    Extracts the frames from the video located at `video_path`.
    """
    video_dir = os.path.dirname(video_path)
    frames_path = os.path.join(dir, "frame_%05d.jpg")

    ffmpeg = FFmpeg().option("i", video_path).option("y").output(frames_path)
    if fps > 0:
        ffmpeg.option("vf", f"fps={fps}")

    try:
        ffmpeg.execute()
        return 0
    except Exception as e:
        print(f"Ran into exception {e}")
        return 1
