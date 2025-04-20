from ffmpeg import FFmpeg
import cv2
import os
import numpy as np

import math

# download_mp4("https://jasonfeng365.github.io/canis/canis-contests.mp4", 'videos/out.mp4')
# extract_frames("videos/", "out.mp4")
def extract_frames(dir: str, video_file: str, fps: int):
	videoPath = os.path.join(dir, video_file)
	framesPath = os.path.join(dir, "frame_%05d.jpg")

	print(videoPath)
	print(framesPath)

	ffmpeg = (
		FFmpeg()
		.option("i", videoPath)
		.option('y')
		.output(framesPath)
	)
	if fps>0: ffmpeg.option('vf', f'fps={fps}')
	ffmpeg.execute()

# Return SUSSY frames of diff
def compare_frames(dir: str, fps: int, chunk_size=100):
	# How long do we wait until we stop trying to merge flashes?
	patience = 10*fps

	frameIdx = 1
	framePath = os.path.join(dir, "frame_%05d.jpg" % frameIdx)
	# There must be at least one frame
	if not os.path.exists(framePath):
		return None
	
	# Initializing prev...
	frame = cv2.imread(framePath)
	# frame = frame.astype(np.int16)
	prev = [
		convolve_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)),
		convolve_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)), 
		# cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			]
	frameIdx += 1

	# Yield intervals (start, delta) of flashing lights
	out = []
	start = None
	end = None
	buffer = []
	countdown = patience
	while os.path.exists(framePath):
		# print(f"Working on ({frameIdx-1}, {frameIdx})")
		frame = cv2.imread(framePath)
		# frame = frame.astype(np.int16)
		new_prev = [
			convolve_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)),
			convolve_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)),
		]
		# If either RGB or HSV say there's a huge change, flag it.
		if diff_bright(prev[1], new_prev[1]) and diff_avg(prev[0], new_prev[0]):
			# Start interval
			if start == None:
				start = frameIdx-1
				end = frameIdx
			else:
				end = frameIdx
				countdown = patience
		
		# Get next frame
		prev = new_prev
		frameIdx += 1
		framePath = os.path.join(dir, "frame_%05d.jpg" % frameIdx)

		if start:
			countdown -= 1
			if countdown == 0:
				buffer.append((math.floor(start/fps), math.ceil((end-start)/fps)))
				# out.append((start/fps, (end-start)/fps))
				# out.append((start, end))
				# Reset the countdown!
				countdown = patience
				start = None
				end = None
		if frameIdx % chunk_size == 0:
			yield buffer
			buffer = []
		# print()

	# If there was one flashing light that kept waiting bc of patience
	if start:
		yield [(math.floor(start/fps), math.ceil((end-start)/fps))]
		

# (74, 132, 3)
# (74, 132, 3)
# (74, 132)

def convolve_frame(frame: np.ndarray, kersize=5):
	h,w,c = frame.shape
	# Pad bottom
	pad_bot = 0
	if h % kersize != 0:
		pad_bot = kersize - (h % kersize)
	# Pad right
	pad_right = 0
	if w % kersize != 0:
		pad_right = kersize - (w % kersize)
	# To allow for the step size to be the entire kernel
	frame = np.pad(frame, pad_width=((0,pad_bot), (0,pad_right), (0,0)), mode="constant", constant_values=0)
	h,w,c = frame.shape

	kernel = np.ones((kersize,kersize), dtype=np.float32)
	out = np.zeros((h//kersize, w//kersize, c), dtype=np.float32)
	for i in range(h//kersize):
		for j in range(w//kersize):
			for k in range(c):
				out[i,j,k] = np.sum(frame[i*kersize:(i+1)*kersize,j*kersize:(j+1)*kersize,k] * kernel)
	return out.astype(np.int16)

def diff_avg(frame1: np.ndarray, frame2: np.ndarray, threshold=1000):
	# 1. Get diff and take abs
	# 2. Take the max of all diffs across pixels' kernels in all channels
	# 3. Summing across all the channels and seeing if this beats threshold
	diff = np.mean(np.abs(frame1-frame2))
	# print("RGB Average Diff", diff)
	if diff >= threshold:
		return True
	return False

def diff_bright(frame1: np.ndarray, frame2: np.ndarray, threshold=2500):
	diff = np.mean(np.abs(frame1[:,:,2]-frame2[:,:,2]))
	# print("Brightness/Value", diff)
	if diff >= threshold:
		return True
	return False

def ff(idx):
	frame = cv2.imread("videos/frame_%05d.jpg" % idx)
	return frame.astype(np.int16)

def test_diff_avg():
	# Literally the same
	print(diff_avg(ff(2), ff(2)))
	# Almost the exact same frame
	print(diff_avg(ff(2), ff(3)))
	# Bomboclaat
	print(diff_avg(ff(6), ff(7)))

# print(compare_frames("videos", 4))

# soba's super stupid test results
# [(7, 8), (67, 68), (91, 92), (97, 98), (98, 99), (99, 100), (101, 102), (114, 115), (135, 136), (149, 150), (204, 205), (234, 235), (260, 261), (261, 262), (262, 263), (275, 276), (276, 277), (277, 278), (278, 279)]
# [(7, 7), (67, 150), (204, 279)]