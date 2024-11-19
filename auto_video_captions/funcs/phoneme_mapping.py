import pandas as pd
import pronouncing as p
import re
import string
import ast

def convert_words_to_phoneme(input_df, phoneme_df):

	final_dict = {}
	id_list = []
	word_list = []
	phoneme_list = []
	w_start_f_list = []
	mouth_list = []
	frame_list = []
	last_frame = []

	for i in range(0, len(input_df.index)):
		translator = str.maketrans('', '', """!"#$%&()*+,-./:;<=>?@[\]^_`{|}~""")
		s = input_df.loc[i]
		if i < len(input_df.index)-1:
			s_next = input_df.loc[i+1]
		else:
			s_next = None

		cur_word = s['word_used'].translate(translator).replace(" ", "")
 
		try:
			cur_phone = p.phones_for_word(cur_word)[0]
		except:
			print(cur_word)
		cur_phone_wo_emph = re.sub(r'\d+', '', cur_phone)

		mouth_map_list = [1]
		frame_map_list = [1]

		for l in cur_phone_wo_emph.split():
			p_dict = phoneme_df[phoneme_df['phoneme'] == l]
			val = p_dict.reset_index().iloc[0]

			mouth_map_list.extend(ast.literal_eval(val['mouth_map']))
			frame_map_list.extend(ast.literal_eval(val['frame_length']))


		if "..." in s['word_used'] or '!' in s['word_used']:
			final_w_map = mouth_map_list + [2, 1]
			final_f_map = frame_map_list + [1, 1]
		else:
			final_w_map = mouth_map_list + [1]
			final_f_map = frame_map_list + [1]

		if s_next is not None:
			if s_next['word_id'] == 0:
				input_df.loc[i+1, 'word_frame_start'] = s_next['word_frame_start']
			else:
				input_df.loc[i+1, 'word_frame_start'] = s['word_frame_start']+sum(final_f_map)-1

		id_list.append(i)
		word_list.append(cur_word)
		phoneme_list.append(cur_phone_wo_emph)
		w_start_f_list.append(s['word_frame_start'])
		mouth_list.append(final_w_map)
		frame_list.append(final_f_map)
		last_frame.append(s['word_frame_start']+sum(final_f_map)-1)



	final_dict['id'] = id_list
	final_dict['word'] = word_list
	final_dict['phoneme'] = phoneme_list
	final_dict['w_start_frame'] = w_start_f_list
	final_dict['mouth_map_list'] = mouth_list
	final_dict['frame_map_list'] = frame_list
	final_dict['last_frame_calc'] = last_frame

	final_df = pd.DataFrame(final_dict)
	print(final_df)

	return final_df

def main():
    transcribed_file = "by_word.csv"
    phoneme_map = "phonetic_mapping.csv"

    input_df = pd.read_csv(transcribed_file)
    phoneme_df = pd.read_csv(phoneme_map)
    final_df = convert_words_to_phoneme(input_df, phoneme_df)
    final_df.to_csv('test_phoneme.csv', index=False)
    
if __name__ == "__main__":
    main() 