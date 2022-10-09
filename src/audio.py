from gtts import gTTS
import moviepy.editor as mpy
import moviepy.audio.fx.all as afx

# Language in which you want to convert
language = 'en'
accent = 'com.au'

FFMPEG_PARAMS = ["-filter:a", "atempo=1.5"]
TMP_AUDIO = "./cache/tmp_audio.mp3"

def create(text, path):
	print("Generating audio...")
	tts = gTTS(text=text, lang=language, slow=False, tld=accent)
	print("Saving audio from GTTS...")
	tts.save(TMP_AUDIO)

	print("Reopening audio as a moviepy object...")
	audioClip = mpy.AudioFileClip(TMP_AUDIO).set_start(0.1)
	audioClip = audioClip.set_end(audioClip.duration - 0.1)
	audioClip = afx.audio_fadeout(afx.audio_fadein(audioClip, 0.1), 0.1)
	print("Resaving audio with effects...")
	audioClip.write_audiofile(path, ffmpeg_params=FFMPEG_PARAMS)
	audioClip.close()
	print("Done with audio!")
