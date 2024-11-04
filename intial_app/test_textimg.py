from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from config import font_path, font_size, asp_ratio, default_color, highlight_color, word_threshold, highlight, sw
import textwrap
import os

def create_text_images(text_obj):
    """Creates a text image with a transparent background."""

    text = text_obj['full_text']
    font = ImageFont.truetype(font_path, font_size)
    ascent, descent = font.getmetrics()
    (width, baseline), (offset_x, offset_y) = font.font.getsize(text)

    x, y = asp_ratio['x'], asp_ratio['y']

    # Create a transparent image
    image = Image.new("RGBA", (x, y), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    words = text.split(' ')
    cwd = os.getcwd()
    if not os.path.exists(f"{cwd}/final_images"):
        os.makedirs(f"{cwd}/final_images")

    x = (x/2)-(width/2)
    draw.text((x, y*.7), text.upper(), fill=(255, 123, 51), font=font, stroke_width=3, stroke_fill='black')
    image.save(f"{cwd}/final_images/{text_obj['text_id']}.png")


    return None

def create_by_word_text_images(text_obj):
    """Creates a text image with a transparent background."""

    if text_obj['words_in_phrase'] > word_threshold:
        text = text_obj['sub_phrase']
        n_w_inphrase = len(text_obj['sub_phrase'].split())
    else:
        text = text_obj['associated_phrase']
        n_w_inphrase = text_obj['words_in_phrase']

    font = ImageFont.truetype(font_path, font_size)
    ascent, descent = font.getmetrics()
    (width, baseline), (offset_x, offset_y) = font.font.getsize(text)

    x, y = asp_ratio['x'], asp_ratio['y']

    # Create a transparent image
    image = Image.new("RGBA", (x, y), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    cwd = os.getcwd()
    if not os.path.exists(f"{cwd}/final_images/by_word"):
        os.makedirs(f"{cwd}/final_images/by_word")

    x = (x/2)-(width/2)
    # Draw the text
    # text_wrapped = ' \n '.join(textwrap.wrap(text, width=35))
    text_wrapped = text
    if text_obj['word_id'] == 0 and n_w_inphrase > 1:

        draw.text((x, y*.7), text_obj['word_used'], fill=(255, 123, 51), font=highlightfont, stroke_width=3, stroke_fill='black')
        x += font.font.getsize(text_obj['word_used'] + " ")[0][0] # Update x position
        remaining_text = text_wrapped.split(f"{text_obj['word_used']} ")[1]
        draw.text((x, y*.7), remaining_text, fill=(255, 255, 255), font=font, stroke_width=3, stroke_fill='black')

    elif text_obj['word_id'] < (n_w_inphrase-1) and n_w_inphrase > 2:

        #phrase before
        phrase_list = text_wrapped.split(f" {text_obj['word_used']} ")

        draw.text((x, y*.7), phrase_list[0].lstrip(), fill=(255, 255, 255), font=font, stroke_width=3, stroke_fill='black')
        x += font.font.getsize(phrase_list[0].lstrip() + " ")[0][0] # Update x position

        #highlited word
        draw.text((x, y*.7), text_obj['word_used'], fill=(255, 123, 51), font=highlightfont, stroke_width=3, stroke_fill='black')
        x += font.font.getsize(text_obj['word_used'] + " ")[0][0] # Update x position

        #what's left
        draw.text((x, y*.7), phrase_list[1].lstrip(), fill=(255, 255, 255), font=font, stroke_width=3, stroke_fill='black')

    else:
        #phrase before
        phrase_list = text_wrapped.split(f"{text_obj['word_used']}")
        draw.text((x, y*.7), phrase_list[0].lstrip(), fill=(255, 255, 255), font=font, stroke_width=3, stroke_fill='black')
        x += font.font.getsize(phrase_list[0].lstrip())[0][0] # Update x position

        #final highlited word
        draw.text((x, y*.7), text_obj['word_used'], fill=(255, 123, 51), font=highlightfont, stroke_width=3, stroke_fill='black')

    image.save(f"{cwd}/final_images/by_word/{text_obj['phrase_id']}_word{text_obj['word_id']}.png")



    return None

def create_by_word_text_images_grow(text_obj, w_list):
    """Creates a text image with a transparent background."""

    if text_obj['words_in_phrase'] > word_threshold:
        text = text_obj['sub_phrase']
        n_w_inphrase = len(text_obj['sub_phrase'].lstrip().split())
    else:
        text = text_obj['associated_phrase']
        n_w_inphrase = text_obj['words_in_phrase']

    font = ImageFont.truetype(font_path, font_size)
    highlightfont = ImageFont.truetype(font_path, highlight)
    ascent, descent = font.getmetrics()
    (width, baseline), (offset_x, offset_y) = font.font.getsize(text)

    x, y = asp_ratio['x'], asp_ratio['y']

    # Create a transparent image
    image = Image.new("RGBA", (x, y), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    cwd = os.getcwd()
    if not os.path.exists(f"{cwd}/final_images/by_word"):
        os.makedirs(f"{cwd}/final_images/by_word")

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

    image.save(f"{cwd}/final_images/by_word/{text_obj['phrase_id']}_word{text_obj['word_id']}.png")

    if ' '.join(w_list) == text.lstrip():
        w_list = []

    return w_list


def extract_meta_from_file(file, by_word):

    df = pd.read_csv(file)
    word_list = []

    for d in range(0, len(df)):
        if by_word:
            # create_by_word_text_images(df.iloc[d])
            word_list = create_by_word_text_images_grow(df.iloc[d], word_list)
        else:
            create_text_images(df.iloc[d])

    return None


def run_image_process(file_name, file_path='', by_word=True):

    if file_path != '':
        file = file_path + file_name
    else:
        file = file_name

    extract_meta_from_file(file, by_word)

    print('Process Complete!')

    return None


