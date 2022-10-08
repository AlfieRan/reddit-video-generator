import moviepy.editor as mpy
import random
import math
import audio

FPS = 60 		# Set to 60 on final
CODEC = "libx264"
PADDING = 0.05

AUDIO_PATH = "./cache/tmp/audio"
AUDIO_ENDING = "mp3"

def split_sentence(words: str):
	parts = [" ".join(words[:len(words)//2]), " ".join(words[len(words)//2:])]
	Phrases = []

	for part in parts:
		words = part.split(" ")
		if len(words) > 15:
			Phrases.extend(split_sentence(words))
		else:
			Phrases.append(part)

	return Phrases

def split_text(text: str):
	Tmp_Sentences = text.replace("\n", ".").replace("\t", " ").replace("  ", " ").split(".")
	Sentences = []

	# This is a horrible way of doing this, but it works
	for sentence in Tmp_Sentences:
		tmpA = sentence.replace("  ", " ").split("?")
		for sentenceA in tmpA:
			tmpB = sentenceA.replace("  ", " ").split("!")
			for sentenceB in tmpB:
				if len(sentenceB) > 1:
					Sentences.append(sentenceB)

	Phrases = []

	for sentence in Sentences:
		words = sentence.replace("  ", " ").split(" ")
		if len(words) < 1:
			continue
		elif len(words) < 15:
			print(f"Adding sentence with {len(words)} words:\t {sentence}\n\n")
			Phrases.append(sentence)
		else:
			print(f"Splitting sentence with {len(words)} words:\t {sentence}\n\n")
			Phrases.extend(split_sentence(words))
				
	for phrase in Phrases:
		words = phrase.split(" ")
		print(f"[{len(words)}] Phrase: {phrase}")

	return Phrases


# Flow for creating a video
# Split text up into sentences/short phrases
# For each sentence/phrase:
# 	Generate audio
# 	Generate video with subtitles
# 	Combine audio and video
# 	Append to final video
# 	Repeat
# Save final video

def create(text, footage_path, video_path):
	Phrases = split_text(text)

	# initialise background video
	full = mpy.VideoFileClip(footage_path)
	audioClips = []
	audioLength = 0

	# Generate audio for phrase
	for i, phrase in enumerate(Phrases):
		print(f"[{i}/{len(Phrases)}] Generating audio...")
		audio.create(phrase, f"{AUDIO_PATH}{i}.{AUDIO_ENDING}")
		audioClips.append(mpy.AudioFileClip(AUDIO_PATH))
		audioLength += audioClips[-1].duration


	for i, phrase in enumerate(Phrases):
		print(f"[{i}/{len(Phrases)}] Generating video...")

	# Create background footage
	start_point = random.uniform(0, full.duration - (audioLength + (PADDING*full.duration)))

	# Set the start and end points of the video to a random point in the footage based on the audio length
	clip = (full.
		subclip(start_point, start_point + audioLength).
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
