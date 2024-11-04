from test_textimg import *
from test import *

def main():
    test_file = "Congratulations_pure.mp3"
    by_word = True
    transcribed_file = "by_word.csv"

    # extract_text_from_audio(test_file)

    run_image_process(transcribed_file, file_path='', by_word=by_word)

    
    
if __name__ == "__main__":
    main() 