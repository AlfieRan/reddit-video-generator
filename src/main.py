import audio;
import video;
import time;

DEMO_TEXT = "Alistair Smith Balls Generator"

AUDIO_PATH = "./cache/audio.mp3"
FOOTAGE_PATH = "./footage/minecraft.mp4"
OUTPUT_PATH = "./output/"

def outPath():
	return OUTPUT_PATH + 'output.mp4'

print("Creating audio...")
audio.create(DEMO_TEXT, AUDIO_PATH)
print("Creating video...")
video.create(AUDIO_PATH, FOOTAGE_PATH, outPath())
print("Done!")
