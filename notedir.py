import os
import os.path
import shutil

def create_repo(repo_path):
	os.mkdir(repo_path, 0o700)

def check_dir(repo_path):
		try:
			if os.access(repo_path, os.F_OK):
				return
			else:
				create_repo(repo_path)
		except Error as err:
			print("Oops!", err)

def clean_out(repo_path):
	try:
		shutil.rmtree(repo_path)
	except FileNotFoundError as err: pass