import os

def check_create(file_path):
	if not os.path.exists(file_path):
		os.makedirs(file_path)

def init(file_paths):
	for file_path in file_paths:
		check_create(file_path)

def clear_dir(dir_path):
	if os.path.exists(dir_path):
		files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
		for file in files:
			os.remove(os.path.join(dir_path, file))
