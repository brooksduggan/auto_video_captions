from funcs import transcribe as t

def main():
	test_path = "C:/Users/btdug/OneDrive/Documents/Python Scripts/"
	test_file = "inaworld_pure.mp3"
	by_word = True
	transcribed_file = "by_word.csv"

	t.transcribe(test_path, test_file, test_path, "new_file_test.csv").transcribe_to_file()

	# run_image_process(transcribed_file, file_path='', by_word=by_word)

	
	
if __name__ == "__main__":
	main() 