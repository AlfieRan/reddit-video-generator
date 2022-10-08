# Setup libraries
import requests
import random
import os
import json
from dotenv import load_dotenv
load_dotenv()

# Setup Constants
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

POST_FILEPATH = "./cache/posts.json"
POST_USED_FILEPATH = "./cache/used_posts.json"
POST_ID_FILEPATH = "./cache/prev_id.json"
VIDEO_ID_FILEPATH = "./cache/prev_vid_ids.json"

SUBREDDITS=['offmychest', 'confession', 'askReddit']

# Setup Globals
HEADERS = {
	'User-Agent': 'Reddit_yt_Bot/0.0.1',
}
LOGGED_IN = False

# ====================================================== UTILS ======================================================
# Converts raw reddit api data to a list of dictionaries that contain only the data we need
def simplify_data(posts):
	prev_ids = get_prev_ids()
	output = []


	for post in posts:
		if post['data']['id'] in prev_ids:
			# if the post has already been used, skip it
			continue
			
		output.append({
			'id': post['data']['id'],
			'created': post['data']['created'],
			'author': post['data']['author'],
			'title': post['data']['title'],
			'content': post['data']['selftext'],
			'subreddit': post['data']['subreddit'],
			'score': post['data']['score'],
			'link': post['data']['url'],
		})
		prev_ids.append(post['data']['id'])
	
	save_prev_ids(prev_ids)
	print(f"Collected, {len(output)} new posts.")
	return output

# ====================================================== FILE HANDLING ===============================================
# Get the previous ids from the cache json file
def get_prev_ids():
	try:
		return json.load(open(POST_ID_FILEPATH))
	except:
		# File doesn't exist, skip
		return []

# Save the previous ids to the cache json file
def save_prev_ids(prev_ids):
	json.dump(prev_ids, open(POST_ID_FILEPATH, 'w'))

# Get the previous posts from the cache json file
def get_saved_posts():
	try:
		return json.load(open(POST_FILEPATH))
	except:
		# File doesn't exist, skip
		return []

# Save the previous posts to the cache json file
def save_posts(posts):
	prev_posts = get_saved_posts()
	prev_posts.extend(posts)
	json.dump(prev_posts, open(POST_FILEPATH, 'w'), indent=4)

def get_used_ids():
	try:
		return json.load(open(VIDEO_ID_FILEPATH))
	except:
		# File doesn't exist, skip
		return []


# Get the used posts from the cache json file
def get_used_posts():
	try:
		return json.load(open(POST_USED_FILEPATH))
	except:
		# File doesn't exist, skip
		return []

# Save the used posts to the cache json file
def save_used_posts(posts):
	json.dump(posts, open(POST_USED_FILEPATH, 'w'), indent=4)

# ====================================================== API ======================================================
# Login function - called once at the start of the program
def login():
	if LOGGED_IN:
		print("Already logged in to reddit api.")
		return

	auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

	data = {
		'grant_type': 'password',
		'username': USERNAME,
		'password': PASSWORD,
	}

	res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=HEADERS)
	TOKEN = res.json()['access_token']
	HEADERS['Authorization'] = f'bearer {TOKEN}'
	print("Logged in to reddit api!")
	LOGGED_IN = True

# Get the hot posts from a subreddit
def get_hot_posts(subreddit):
	res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/hot', headers=HEADERS)
	posts = res.json()['data']['children']
	return simplify_data(posts)

# Get the new posts from a random subreddit of the SUBREDDITS list
def get_hot_posts_random():
	subreddit = random.choice(SUBREDDITS)
	return get_hot_posts(subreddit)


# ====================================================== MAIN ======================================================
def get_more_posts():
	# login to the reddit api
	login()
	# get the hot posts from a random subreddit
	posts = get_hot_posts_random()
	# save the posts to the cache
	save_posts(posts)

# Get a random post from cache
def load_random_post():
	posts = get_saved_posts()

	if len(posts) < 5:
		# if there are less than 5 posts in the cache, get more
		get_more_posts()
		posts = get_saved_posts()

	# return a random post
	return random.choice(posts)

# mark a post as used in a video so it doesn't get used again
def mark_post_as_used(post):
	post_id = post['id']
	# get the ids of the used posts
	used_ids = get_used_ids()
	# add the new id to the list
	used_ids.append(post_id)
	# save the list
	json.dump(used_ids, open(VIDEO_ID_FILEPATH, 'w'), indent=4)

	# get the posts that have been used
	used_posts = get_used_posts()
	# find the post with the matching id
	posts = get_saved_posts()
	for index, post in enumerate(posts):
		if post['id'] == post_id:
			# add the post to the used posts list
			posts.pop(index)
			used_posts.append(post)
			break

	# save the posts
	save_posts(posts)
	save_used_posts(used_posts)
	
def get_post_text(post):
	return f"{post['title']}. {post['content']}"

def get_post_title(post):
	return f"{post['title']}"