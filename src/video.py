import moviepy.editor as mpy
import random
import math

FPS = 60 		# Set to 60 on final
CODEC = "libx264"
PADDING = 0.1

def create(audio_path, footage_path, video_path):
	print("Reloading audio...")
	audioClip = mpy.AudioFileClip(audio_path)
	print("Generating video...")

	# Create video clip
	full = mpy.VideoFileClip(footage_path)
	start_point = random.uniform(0, full.duration - (audioClip.duration + (PADDING*full.duration)))
	W, H = full.size

	clip = (full.
		subclip(start_point, start_point + audioClip.duration).
		set_audio(audioClip).
		set_duration(audioClip.duration).
		crop(x_center=math.floor(W/2), y_center=math.floor(H/2), width=H*9/16, height=H))

	print("Saving video...")
	clip.write_videofile(video_path, fps=FPS, codec=CODEC)
	print("Done with video!")