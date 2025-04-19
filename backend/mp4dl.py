from ffmpeg import FFmpeg

def download_mp4(url, outputFile, area=10000):
	# -vf "scale=2*floor(sqrt(1000*iw/ih)/2):2*floor(1000/sqrt(1000*iw/ih)/2),setsar=1:1"
	widthEq = f'2*floor(sqrt({area}*iw/ih)/2)'
	heightEq = f'2*floor({area}/sqrt({area}*iw/ih)/2)'
	vf = f'scale={widthEq}:{heightEq},setsar=1:1'
	print(vf)
	ffmpeg = (
		FFmpeg()
		.option("i", url)
		.option("vf", vf)
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

	print(" ".join(ffmpeg.arguments))
	# print(ffmpeg.)

	ffmpeg.execute()

