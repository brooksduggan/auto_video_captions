import os
import logging as log
from moviepy.editor import VideoFileClip

def file_path_exists(path):

	return os.path.exists(path)

def file_path_create(path):

	if file_path_exists(path) == False:
		try:
			os.makedirs(path)
		except OSError as error:
			log.error(error) 

def get_audio_from_video(input_path, output_path, output_name):
	video_clip = VideoFileClip(input_path)

	# Extract the audio from the video clip
	audio_clip = video_clip.audio

	# Write the audio to a separate file
	audio_clip.write_audiofile(output_path+f"/{output_name}_audio.mp3")

	# Close the video and audio clips
	audio_clip.close()
	video_clip.close()

def remove_spaces_and_punctuation(text):
	"""Removes all spaces and punctuation from a given string."""

	# Create a translation table to remove punctuation
	translator = str.maketrans('', '', """!"#$%&'()*+,./:;<=>?@[\]^`{|}~""")

	# Remove punctuation and spaces
	text = text.translate(translator).replace(" ", "")

	return text