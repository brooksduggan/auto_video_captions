import whisper
import pandas as pd
import math
import string
from config import word_threshold

def get_text(audio_name):
	model = whisper.load_model("turbo")
	result = model.transcribe(audio_name, language='English')

	return result

def create_individual_texts(text_obj, frame_rate):

	out_dict = {}
	text_id = []
	full_text = []
	t_f_l = []
	w_c = []
	f_p_w = []
	line_start = []
	line_end = []
	for t in text_obj['segments']:
		w_time = t['end'] - t['start']
		w_frames = math.ceil(w_time * frame_rate)
		w_count = len(t['text'].replace(',','').split(' '))
		f_per_w = math.ceil(w_frames/w_count)
		frame_start = math.floor(t['start'] * frame_rate)
		frame_end = math.floor(t['end'] * frame_rate)

		text_id.append(f"captions_{t['id']}")
		full_text.append(t['text'].lstrip())
		t_f_l.append(w_frames)
		w_c.append(w_count)
		f_p_w.append(f_per_w)
		line_start.append(frame_start)
		line_end.append(frame_end)

		if t['id'] == 0:
			df = pd.DataFrame(create_by_word_texts(t, frame_rate, w_frames, frame_start, frame_end))
		else:
			df = pd.concat([df,pd.DataFrame(create_by_word_texts(t, frame_rate, w_frames, frame_start, frame_end))])
	df.to_csv('by_word.csv', index=False)

	out_dict['text_id'] = text_id
	out_dict['full_text'] = full_text
	out_dict['text_frame_len'] = t_f_l
	out_dict['word_count'] = w_c
	out_dict['frame_per_word'] = f_p_w
	out_dict['line_start'] = line_start
	out_dict['line_end'] = line_end


	return out_dict

def create_by_word_texts(text_obj, frame_rate, w_frames, frame_start, frame_end):

	text = text_obj['text']

	# Remove punctuation and spaces
	word_list = text.lstrip().split()
	phrase_len = len(remove_spaces_and_punctuation(text))
	total_frames = frame_end - frame_start
	word_start = frame_start

	by_word_dict = {}
	word_id = []
	word = []
	word_total = []
	associated_phrase = []
	phrase_id = []
	word_weight = []
	word_frames = []
	word_frame_start = []
	word_frame_end = []
	phrase_start = []
	phrase_end = []
	sub_phrase = []
	final_subp = []


	for i, t in enumerate(word_list):
		w_weight = len(t)/phrase_len
		w_frames = math.ceil(w_weight * total_frames)


		word_f_end = word_start + w_frames

		word_id.append(i)
		associated_phrase.append(text.upper())
		word.append(t.upper())
		word_total.append(len(word_list))
		phrase_start.append(frame_start)
		phrase_end.append(frame_end)
		word_weight.append(w_weight)
		word_frames.append(w_frames)
		word_frame_start.append(word_start)
		word_frame_end.append(word_f_end)
		word_start = word_f_end
		n = word_threshold
		if len(word_list) > n:
			splt = math.floor(i/n)
			part = [word_list[i:i + n] for i in range(0, len(word_list), n)]
			sub_phrase.append(' '.join(part[splt]).upper())
			phrase_id.append(f"text_{text_obj['id']}_{splt}")
		else:
			sub_phrase.append(None)
			phrase_id.append(f"text_{text_obj['id']}")



	by_word_dict['word_id'] = word_id
	by_word_dict['phrase_id'] = phrase_id
	by_word_dict['associated_phrase'] = associated_phrase
	by_word_dict['sub_phrase'] = sub_phrase
	by_word_dict['word_used'] = word
	by_word_dict['words_in_phrase'] = word_total
	by_word_dict['phrase_f_start'] = phrase_start
	by_word_dict['phrase_f_end'] = phrase_end
	by_word_dict['word_weight'] = word_weight
	by_word_dict['word_frames'] = word_frames
	by_word_dict['word_frame_start'] = word_frame_start
	by_word_dict['word_frame_end'] = word_frame_end

	return by_word_dict

def remove_spaces_and_punctuation(text):
  """Removes all spaces and punctuation from a given string."""

  # Create a translation table to remove punctuation
  translator = str.maketrans('', '', string.punctuation)

  # Remove punctuation and spaces
  text = text.translate(translator).replace(" ", "")

  return text

def create_csv(meta_dict, file_name, file_path):
	

	df = pd.DataFrame(meta_dict)

	df.to_csv(f'{file_path}transcribe_res.csv', index=False)

	return None

def create_srt(meta_dict):


	return None


def extract_text_from_audio(file_name, file_path='', frame_rate=20):

	if file_path != '':
		file = file_path + file_name
	else:
		file = file_name

	res = get_text(file)

	out_dict = create_individual_texts(res, frame_rate)

	print(out_dict)

	create_csv(out_dict, f'{file_name}_transcribe_res.csv', file_path)

	return None

