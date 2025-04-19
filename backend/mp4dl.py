from ffmpeg import FFmpeg

def download_mp4(url, outputFile):
	ffmpeg = (
		FFmpeg()
		.option("i", url)
		.option('y')
		.output(
			outputFile
			# "output.mp4",
			# {"codec:v": "libx264"},
			# vf="scale=1280:-1",
			# preset="veryslow",
			# crf=24,
		)
	)

	ffmpeg.execute()

