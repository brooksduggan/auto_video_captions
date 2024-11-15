import os
import logging as log

def is_valid_path(path):
	"""
	Check if a given path is valid.

	Args:
		path (str): The path to check.

	Returns:
		bool: True if the path is valid, False otherwise.
	"""

	try:
		os.stat(path)
		return True
	except OSError:
		return False

def file_path_exists(path):

	if is_valid_path(path):
		return os.path.exists(path)
	else:
		log.error("File path does not exist and is not valid!")
		return Exception

def file_path_create(path):

	if file_path_exists(path) == False:
		try:
			os.mkdir(path)
		except OSError as error:
			log.error(error)   