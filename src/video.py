import moviepy.editor as mpy
import random
import math

FPS = 60 		# Set to 60 on final
CODEC = "libx264"
PADDING = 0.1

def create(audio_path, footage_path, video_path):
	# Get audio
	print("Reloading audio...")
	audioClip = mpy.AudioFileClip(audio_path)
	print("Generating video...")

	# Create background footage
	full = mpy.VideoFileClip(footage_path)
	start_point = random.uniform(0, full.duration - (audioClip.duration + (PADDING*full.duration)))

	# Set the start and end points of the video to a random point in the footage based on the audio length
	clip = (full.
		subclip(start_point, start_point + audioClip.duration).
		set_audio(audioClip).
		set_duration(audioClip.duration))

	# Crop the video to the correct aspect ratio
	cropped = None
	if audioClip.duration > 58:
		print("Audio is too long for a short, making a long...")
		cropped = crop_long(clip)
	else:
		cropped = crop_short(clip)

	# Save the video
	print("Saving video...")
	cropped.write_videofile(video_path, fps=FPS, codec=CODEC)
	print("Done with video!")
	full.close()
	clip.close()
	cropped.close()

def crop_short(clip):
	W, H = clip.size
	return (clip.crop(x_center=math.floor(W/2), y_center=math.floor(H/2), width=H*9/16, height=H))

def crop_long(clip):
	W, H = clip.size
	return (clip.crop(x_center=math.floor(W/2), y_center=math.floor(H/2), width=H*16/9, height=H))
