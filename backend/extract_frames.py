from ffmpeg import FFmpeg
import cv2
import os
import numpy as np

# download_mp4("https://jasonfeng365.github.io/canis/canis-contests.mp4", 'videos/out.mp4')
# extract_frames("videos/", "out.mp4")
def extract_frames(path, videoName, fps=-1):
	if path[-1] != '/': path += '/'
	videoPath = path + videoName
	framesPath = path + "frame_%05d.jpg"

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
def compare_frames(path):
	frameIdx = 1
	framePath = os.path.join(path, "frame_%05d.jpg" % frameIdx)
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

	# List of diffs from each of the image formats
	out = []
	while os.path.exists(framePath):
		print(f"Working on ({frameIdx-1}, {frameIdx})")
		frame = cv2.imread(framePath)
		# frame = frame.astype(np.int16)
		new_prev = [
			convolve_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)),
			convolve_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)),
		]
		# If either RGB or HSV say there's a huge change, flag it.
		if diff_frames(prev[0], new_prev[0]) or diff_frames(prev[1], new_prev[1]):
			out.append((frameIdx-1, frameIdx))
		
		# Get next frame
		prev = new_prev
		frameIdx += 1
		framePath = os.path.join(path, "frame_%05d.jpg" % frameIdx)
		print()
	return out

# (74, 132, 3)
# (74, 132, 3)
# (74, 132)

# Default no kernel (just 1 pixel)
def convolve_frame(frame, kersize=5):
	kernel = np.ones((kersize,kersize), dtype=np.float32)
	h,w,c = frame.shape
	out = np.zeros((h - kersize + 1, w - kersize + 1, c), dtype=np.float32)
	for i in range(h - kersize + 1):
		for j in range(w - kersize + 1):
			for k in range(c):
				out[i,j,k] = np.sum(frame[i:i+kersize, j:j+kersize, k] * kernel)
	return out.astype(np.int16)

def diff_frames(frame1: np.ndarray, frame2: np.ndarray, threshold=5500):
	_,_,c = frame1.shape
	# 1. Get diff and take abs
	# 2. Take the max of all diffs across pixels' kernels in all channels
	# 3. Summing across all the channels and seeing if this beats threshold
	diff = np.max(np.abs(frame1[:,:,:]-frame2[:,:,:]))
	val = np.sum(diff)
	print("Max difference:", diff)
	print(f"Found diff:", val)
	if np.sum(np.max(np.abs(frame1[:,:,:]-frame2[:,:,:]))) >= threshold:
		return True
	return False

def ff(idx):
	frame = cv2.imread("videos/frame_%05d.jpg" % idx)
	return frame.astype(np.int16)

def test_diff_frames():
	# Literally the same
	print(diff_frames(ff(2), ff(2)))
	# Almost the exact same frame
	print(diff_frames(ff(2), ff(3)))
	# Bomboclaat
	print(diff_frames(ff(6), ff(7)))

# test_diff_frames()
print(compare_frames("videos"))