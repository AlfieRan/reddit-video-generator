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
			print(f"Adding sentence with {len(words)} words:\t {sentence}")
			Phrases.append(sentence)
		else:
			print(f"Splitting sentence with {len(words)} words:\t {sentence}")
			Phrases.extend(split_sentence(words))
				
	for phrase in Phrases:
		words = phrase.split(" ")
		print(f"[{len(words)}] Phrase: {phrase}")

	return Phrases

def captionise_text(text: str):
	if len(text) < 30:
		return text
	
	words = text.split(" ")
	output = ""
	line = ""
	for word in words:
		# 29 rather than 30 to account for the space
		if len(line) + len(word) < 29:
			line += f"{word} "
		else:
			output += f"{line}\n"
			line = f"{word} "

	if len(line) > 0:
		output += line
	
	return output

def makeText(text: str, fontSize: int = 50):
	return mpy.TextClip(text, fontsize=fontSize, color="white", stroke_color="black", stroke_width=2, font="Arial-Bold", method='label')

# Flow for creating a video
# Split text up into sentences/short phrases
# For each sentence/phrase:
# 	1. Generate audio
# 	2. Generate video with audio
# 	3. Add subtitles to video
# 	4. Append to final video
# 	5. Repeat
# Save final video

def create(text, footage_path, video_path):
	# Split text up into sentences/short phrases
	Phrases = split_text(text)

	# initialise background video
	full = mpy.VideoFileClip(footage_path)
	clips = []
	audioClips = []
	audioLength = 0

	# 1. Generate audio for phrase
	for i, phrase in enumerate(Phrases):
		print(f"[{i}/{len(Phrases)-1}] Generating audio...")
		audioClipPath = f"{AUDIO_PATH}{i}.{AUDIO_ENDING}"
		audio.create(phrase, audioClipPath)
		# audio gets saved and reloaded here to apply ffmpeg effects
		audioClipTmp = mpy.AudioFileClip(audioClipPath)
		audioClipTmp = audioClipTmp.set_start(0.1).set_end(audioClipTmp.duration - 0.1)
		audioClips.append(audioClipTmp)
		audioLength += audioClips[-1].duration

	start_point = random.uniform((PADDING*full.duration), full.duration - (audioLength + (PADDING*full.duration)))

	
	for i, phrase in enumerate(Phrases):
		# 2. Generate video with audio
		print(f"[{i}/{len(Phrases)-1}] Generating video...")
		audioClip = audioClips[i]

		clip = (full.
			subclip(start_point, start_point + audioClip.duration).
			set_audio(audioClip).
			set_duration(audioClip.duration))
			
		# increase start point for next clip
		start_point += audioClip.duration

		# Crop the video to the correct aspect ratio
		cropped = None
		if audioLength > 58:
			print("Audio is too long for a short, making a long...")
			cropped = crop_long(clip)
		else:
			cropped = crop_short(clip)

		# 3. Add subtitles to video
		print(f"[{i}/{len(Phrases)-1}] Adding subtitles...")
		subtitles = (makeText(captionise_text(phrase)).
						set_position(("center", "center")))

		# Append to video
		print(f"[{i}/{len(Phrases)-1}] Appending to video...")
		finalClip = mpy.CompositeVideoClip([cropped, subtitles])
		finalClip.duration = audioClip.duration
		clips.append(finalClip)

	# 4. Append to final video
	print("Appending clips to final video...")
	video = mpy.concatenate_videoclips(clips)
	additional_text = (makeText("@MyBalls", fontSize=80).set_duration(video.duration).set_position(("center", 0.75), relative=True))
	final = mpy.CompositeVideoClip([video, additional_text])

	# Save the video
	print("Saving video...")
	final.write_videofile(video_path, fps=FPS, codec=CODEC)
	print("Done with video!")
	full.close()
	final.close()
	# should be closed automatically, but close large videos just in case

def crop_short(clip):
	W, H = clip.size
	return (clip.crop(x_center=math.floor(W/2), y_center=math.floor(H/2), width=H*9/16, height=H))

def crop_long(clip):
	W, H = clip.size
	return (clip.crop(x_center=math.floor(W/2), y_center=math.floor(H/2), width=H*16/9, height=H))
