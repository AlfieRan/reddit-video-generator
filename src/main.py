import video;
import reddit;
import files;

FOOTAGE_PATH = "./footage/minecraft.mp4"
OUTPUT_PATH = "./output/"

REQUIRED_FOLDERS = ['./cache', './cache/tmp', './footage', './output']

def outPath(post):
	parsed_title = reddit.get_post_title(post).replace("/", "-")
	return f"{OUTPUT_PATH}{parsed_title}.mp4"


def main():
	print("Getting reddit post...")
	files.init(REQUIRED_FOLDERS)
	files.clear_dir("./cache/tmp")
	# post = reddit.get_specific_post("xy0rgc") # Testing, short post
	post = reddit.load_random_post() # Load a reddit post from the api
	text = reddit.get_post_text(post) # Get the text from the post
	print("Creating video...")
	video.create(text, FOOTAGE_PATH, outPath(post)) # Create a video from the text
	print("Marking post as used...")
	# reddit.mark_post_as_used(post) # Mark the post as used
	print("Done!")

if __name__ == "__main__":
	main()

