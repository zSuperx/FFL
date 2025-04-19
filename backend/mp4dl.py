from ffmpeg import FFmpeg


def scale_video(url, outputFile, area=10000):
	# -vf scale=2*floor(sqrt(1000*iw/ih)/2):2*floor(1000/sqrt(1000*iw/ih)/2),setsar=1:1
	widthEq = f"'2*floor(min(iw,sqrt({area}*iw/ih))/2)'"
	heightEq = f"'2*floor(min(ih,{area}/sqrt({area}*iw/ih))/2)'"
	vf = f"scale={widthEq}:{heightEq},setsar=1:1"
	print(vf)
	ffmpeg = FFmpeg().option("i", url).option("vf", vf).option("y").output(outputFile)

	ffmpeg.execute()
