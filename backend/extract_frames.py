from ffmpeg import FFmpeg

# download_mp4("https://jasonfeng365.github.io/canis/canis-contests.mp4", 'videos/out.mp4')
# extract_frames("videos/", "out.mp4")
def extract_frames(path, videoName, fps=1):
	if path[-1] != '/': path += '/'
	videoPath = path + videoName
	framesPath = path + "frame_%05d.jpg"

	print(videoPath)
	print(framesPath)

	ffmpeg = (
		FFmpeg()
		.option("i", videoPath)
		.option('y')
		.option('vf', f'fps={fps}')
		.output(framesPath)
	)

	ffmpeg.execute()