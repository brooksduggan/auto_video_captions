from funcs import transcribe as t
from funcs import helpers as h
from funcs import caption_create as cc
from funcs.config import *

def main():

	for p in [input_path, output_path, image_path]:
		h.file_path_create(p)
  
	# t.transcribe(input_path, audio_file, output_path, transcript_fn+".csv").transcribe_to_file()

	while True:
		if input('Is the transcription correct? (Y/N)') == 'N':
			continue
		else:
			cc.createCaptions(transcript_fn, output_path, image_path).process_images()
			break

	
	
if __name__ == "__main__":
	main() 