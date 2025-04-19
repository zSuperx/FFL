import os
import time

from mp4dl import download_mp4
from ytdl import download_yt_vid

from extract_frames import extract_frames

def getDirectory(url):
	ms = int(round(time.time() * 1000))
	h = hash(url)

	directory = f"videos/{ms}_{h}/"
	os.makedirs(directory, exist_ok=True)
	return directory

def downloadVideo(url, videoName): download_mp4(url, videoName, 1000000)
def downloadYoutube(url, videoName): download_yt_vid(url, videoName)


def process(url, videoType):
	# How risky is this video?
	severity = 0
	# List of 2-length lists: range where flashing lights occur
	timestamps = []

	directory = getDirectory(url)
	videoName = directory + "video.mp4"

	if videoType=="youtube": downloadYoutube(url, videoName)
	elif videoType=="video": downloadVideo(url, videoName)

	extract_frames(directory, "video.mp4", 1)

	res = {
		"severity": severity,
		"timestamps": timestamps
	}
	return res