import os
import logging as log

def file_path_exists(path):

	return os.path.exists(path)

def file_path_create(path):

	if file_path_exists(path) == False:
		try:
			os.makedirs(path)
		except OSError as error:
			log.error(error)   