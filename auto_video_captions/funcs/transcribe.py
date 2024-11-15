import whisper_timestamped as wt
import pandas as pd
import math
import logging as log
import json
# from config import word_threshold, frame_rate

class transcribe:
	"""
	"""

	def __init__(self, audio_path, audio_name, output_path, output_name):
	
		self.audio_path = audio_path
		self.audio_name = audio_name
		self.output_path = output_path
		self.output_name = output_name
		self.frame_rate = 20
		self.w_threshold = 3
		self.org_dict = {}

	def transcribe_to_file(self):
		self.transcribe_audio()
		self.organize_text()
		self.create_csv()
		

	def transcribe_audio(self):
		# model = wt.load_model("turbo")
		# self.transcription = wt.transcribe(model, self.audio_path+self.audio_name, language='English')
		log.info("Retrieving text from audio...")
		with open(self.output_path+"testoutput.json", "r") as file:
			# Write the string to the file
			self.transcription = json.load(file)

		return None


	def organize_text(self):
		out_dict = {}
		text_id = []
		full_text = []
		seg_time = []
		t_f_l = []
		w_c = []
		line_start = []
		line_end = []
		word_id = []
		word = []
		phrase_id = []
		word_frames = []
		word_frame_start = []
		word_frame_end = []
		sub_phrase = []
		for seg in self.transcription['segments']:
			for i, w in enumerate(seg['words']):
				word_list = seg['text'].lstrip().split()
				# Segment specific calculations
				s_time = seg['end'] - seg['start']
				s_frames = math.ceil(s_time * self.frame_rate)
				w_count = len(seg['text'].replace(',','').split(' '))
				seg_frame_start = math.floor(seg['start'] * self.frame_rate)
				seg_frame_end = math.ceil(seg['end'] * self.frame_rate)

				# Word specific calculations
				w_time = w['end'] - w['start']
				w_frames = math.ceil(w_time * self.frame_rate)
				w_frame_start = math.floor(w['start'] * self.frame_rate)
				w_frame_end = math.ceil(w['end'] * self.frame_rate)

				text_id.append(f"seg_{seg['id']}")
				full_text.append(seg['text'].lstrip())
				seg_time.append(s_time)
				t_f_l.append(s_frames)
				w_c.append(w_count)
				line_start.append(seg_frame_start)
				line_end.append(seg_frame_end)
	
				word_id.append(i)
				word.append(w['text'].upper())
				word_frames.append(w_frames)
				word_frame_start.append(w_frame_start)
				word_frame_end.append(w_frame_end)
				
				if len(word_list) > self.w_threshold:
					splt = math.floor(i/self.w_threshold)
					part = [word_list[i:i + self.w_threshold] for i in range(0, len(word_list), self.w_threshold)]
					sub_phrase.append(' '.join(part[splt]).upper())
					phrase_id.append(f"seg_{seg['id']}_{splt}")
				else:
					sub_phrase.append(None)
					phrase_id.append(f"seg_{seg['id']}")
     
		out_dict['segment_id'] = text_id 
		out_dict['full_text'] = full_text
		out_dict['segment_time'] = seg_time
		out_dict['text_frame_len'] = t_f_l
		out_dict['word_count'] = w_c
		out_dict['line_start'] = line_start
		out_dict['line_end'] = line_end


		out_dict['word_id'] = word_id
		out_dict['phrase_id'] = phrase_id
		out_dict['sub_phrase'] = sub_phrase
		out_dict['word_used'] = word
		out_dict['word_frame_start'] = word_frame_start
		out_dict['word_frame_end'] = word_frame_end
		self.org_dict = out_dict

		return out_dict

	def create_csv(self):
			log.info("Creating CSV output...")
			df = pd.DataFrame(self.org_dict)
			df.to_csv(self.output_path+self.output_name, index=False)