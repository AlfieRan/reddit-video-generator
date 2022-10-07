import audio;
import video;
import reddit;

AUDIO_PATH = "./cache/audio.mp3"
FOOTAGE_PATH = "./footage/minecraft.mp4"
OUTPUT_PATH = "./output/"

def outPath(post):
	return f"{OUTPUT_PATH}{reddit.get_post_title(post)}.mp4"

def main():
	print("Getting reddit post...")
	post = reddit.load_random_post()
	text = reddit.get_post_text(post)

	print("Creating audio...")
	audio.create(text, AUDIO_PATH)

	print("Creating video...")
	video.create(AUDIO_PATH, FOOTAGE_PATH, outPath(post))

	print("Marking post as used...")
	reddit.mark_post_as_used(post)

	print("Done!")

if __name__ == "__main__":
	main()