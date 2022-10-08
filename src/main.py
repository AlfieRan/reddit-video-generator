import video;
import reddit;

FOOTAGE_PATH = "./footage/minecraft.mp4"
OUTPUT_PATH = "./output/"

def outPath(post):
	return f"{OUTPUT_PATH}{reddit.get_post_title(post)}.mp4"




def main():
	print("Getting reddit post...")
	post = reddit.load_random_post() # Load a reddit post from the api
	text = reddit.get_post_text(post) # Get the text from the post
	print("Creating video...")
	video.create(text, FOOTAGE_PATH, outPath(post)) # Create a video from the text
	print("Marking post as used...")
	reddit.mark_post_as_used(post) # Mark the post as used
	print("Done!")

if __name__ == "__main__":
	main()






