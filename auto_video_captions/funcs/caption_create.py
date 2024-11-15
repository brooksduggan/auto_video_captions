from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from config import font_path, font_size, asp_ratio, default_color, highlight_color, word_threshold, highlight, sw
import textwrap
import os

class createCaptions:
	"""
	"""
	def __init__(self, transcript_fn, transcript_path, img_output_path):
		self.transcript_fn = transcript_fn
		self.transcript_path = transcript_path
		self.full_transcript_path = self.transcript_path + self.transcript_fn
		self.img_output_path = img_output_path

	def process_images(self):

		self._extract_meta_from_file()

		print('Process Complete!')

		return None

	def _extract_meta_from_file(self):

			df = pd.read_csv(self.full_transcript_path + ".csv")
			word_list = []

			for d in range(0, len(df)):
				word_list = self._create_by_word_text_images_grow(df.iloc[d], word_list)

			return None

	def _create_text_images(text_obj):
		"""Creates a text image with a transparent background."""

		text = text_obj['full_text']
		font = ImageFont.truetype(font_path, font_size)
		# ascent, descent = font.getmetrics()
		(width, baseline), (offset_x, offset_y) = font.font.getsize(text)

		x, y = asp_ratio['x'], asp_ratio['y']

		# Create a transparent image
		image = Image.new("RGBA", (x, y), (0, 0, 0, 0))
		draw = ImageDraw.Draw(image)

		cwd = os.getcwd()
		if not os.path.exists(f"{cwd}/final_images"):
			os.makedirs(f"{cwd}/final_images")

		x = (x/2)-(width/2)
		draw.text((x, y*.7), text.upper(), fill=(255, 123, 51), font=font, stroke_width=3, stroke_fill='black')
		image.save(f"{cwd}/final_images/{text_obj['text_id']}.png")


		return None

	def _create_by_word_text_images_grow(self, text_obj, w_list):
		"""Creates a text image with a transparent background."""

		if text_obj['words_in_phrase'] > word_threshold:
			text = text_obj['sub_phrase']
			n_w_inphrase = len(text_obj['sub_phrase'].lstrip().split())
		else:
			text = text_obj['associated_phrase']
			n_w_inphrase = text_obj['words_in_phrase']

		font = ImageFont.truetype(font_path, font_size)
		highlightfont = ImageFont.truetype(font_path, highlight)
		# ascent, descent = font.getmetrics()
		(width, baseline), (offset_x, offset_y) = font.font.getsize(text)

		x, y = asp_ratio['x'], asp_ratio['y']

		# Create a transparent image
		image = Image.new("RGBA", (x, y), (0, 0, 0, 0))
		draw = ImageDraw.Draw(image)

		x = (x/2)-(width/2)
		# Draw the text
		# text_wrapped = ' \n '.join(textwrap.wrap(text, width=35))
		text_wrapped = text.lstrip()
		if w_list == []:
			active_x = x
			x += font.font.getsize(text_obj['word_used'] + " ")[0][0] # Update x position
			w_list.append(text_obj['word_used'])
			remaining_text = text_wrapped.split(' ')[len(w_list):n_w_inphrase]
			draw.text((x, y*.7), ' '.join(remaining_text), fill=default_color, font=font, stroke_width=sw, stroke_fill='black', align='center')
			draw.text((active_x, y*.7), text_obj['word_used'], fill=highlight_color, font=highlightfont, stroke_width=sw, stroke_fill='black', align='center')

		elif w_list != [] and n_w_inphrase >= 2:

			draw.text((x, y*.7), ' '.join(w_list), fill=default_color, font=font, stroke_width=sw, stroke_fill='black', align='center')
			x += font.font.getsize(' '.join(w_list) + " ")[0][0] # Update x position
			active_x = x
			x += font.font.getsize(text_obj['word_used'] + " ")[0][0] # Update x position
			w_list.append(text_obj['word_used'])

			remaining_text = text_wrapped.split(' ')[len(w_list):n_w_inphrase]
			draw.text((x, y*.7), ' '.join(remaining_text), fill=default_color, font=font, stroke_width=sw, stroke_fill='black', align='center')
			draw.text((active_x, y*.7), text_obj['word_used'], fill=highlight_color, font=highlightfont, stroke_width=sw, stroke_fill='black', align='center')

		elif len(w_list) == n_w_inphrase:
			#phrase before
			draw.text((x, y*.7), ' '.join(w_list), fill=default_color, font=font, stroke_width=sw, stroke_fill='black', align='center')
			x += font.font.getsize(' '.join(w_list) + " ")[0][0] # Update x position

			draw.text((x, y*.7), text_obj['word_used'], fill=highlight_color, font=highlightfont, stroke_width=sw, stroke_fill='black', align='center')
			x += font.font.getsize(text_obj['word_used'] + " ")[0][0] # Update x position
			w_list.append(text_obj['word_used'])

		image.save(f"{self.img_output_path}/{text_obj['phrase_id']}_word{text_obj['word_id']}.png")

		if ' '.join(w_list) == text.lstrip():
			w_list = []

		return w_list


