from funcs import transcribe as t
from funcs import helpers as h
from funcs import caption_create as cc

def main():
	input_path = "C:/Users/btdug/OneDrive/Documents/Python Scripts/"
	output_path = "C:/Users/btdug/OneDrive/Documents/Python Scripts/test_output/"
	image_path = output_path + "caption_imgs/"
	test_file = "inaworld_pure.mp3"
	transcript_fn = "new_file_test"

	for p in [input_path, output_path]:
		h.file_path_create(p)
  
	t.transcribe(input_path, test_file, input_path, transcript_fn+".csv").transcribe_to_file()

	cc.createCaptions(transcript_fn, input_path, image_path).process_images()

	
	
if __name__ == "__main__":
	main() 