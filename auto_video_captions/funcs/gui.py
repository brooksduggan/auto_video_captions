import tkinter as tk
import pandas as pd
from config import *
import math

def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def save_csv(root, df, file_path):
    df.to_csv(file_path, index=False)
    root.destroy()

def create_table(df, frame):
    df = df[['full_text', 'segment_id']].drop_duplicates()
    for index, row in df.iterrows():
        segment_id = tk.Entry(frame)
        segment_id.insert(0, row['segment_id'])
        segment_id.grid(row=index, column=0)

        full_text = tk.Entry(frame)
        full_text.insert(0, row['full_text'])
        full_text.grid(row=index, column=1)

def update_check(df):

    for i, r in df.iterrows():
        start = r['word_id']//word_threshold*word_threshold
        end = ((r['word_id']//word_threshold)+1)*word_threshold
        word_list = r['full_text'].lstrip().upper().split()
        new_sub = ' '.join(word_list[start:end])
        if r['sub_phrase'] != new_sub:
            df.loc[df['sub_phrase'] == r['sub_phrase'], 'sub_phrase'] = new_sub
            df.loc[(df['word_id'] == r['word_id']) & (df['phrase_id'] == r['phrase_id']), 'word_used'] = word_list[r['word_id']]

    return df


def save_changes(root, df, frame):
    update_df = df[['full_text', 'segment_id']].drop_duplicates()
    for index, row in update_df.iterrows():
        segment_id = frame.grid_slaves(row=index, column=0)
        full_text = frame.grid_slaves(row=index, column=1)

        df.loc[df['segment_id'] == segment_id[0].get(), 'full_text'] = full_text[0].get()

    final_df = update_check(df)

    save_csv(root, final_df, "")  # Replace 'updated_file.csv' with your desired output file

def main():
    file_path = ""  # Replace with your actual file path
    df = load_csv(file_path)

    root = tk.Tk()
    root.title("CSV Editor")

    frame = tk.Frame(root)
    frame.pack(fill='both', expand=1)

    my_canvas = tk.Canvas(frame)
    my_canvas.pack(side='left', fill='both', expand=1)

    scrollbar = tk.Scrollbar(frame, orient='vertical', command=my_canvas.yview)
    scrollbar.pack( side = "right", fill="y" )

    my_canvas.configure(yscrollcommand=scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))

    scnd_frame = tk.Frame(my_canvas)

    my_canvas.create_window((0,0), window=scnd_frame, anchor='nw')

    create_table(df, scnd_frame)

    save_button = tk.Button(root, text="Save Changes", command=lambda: save_changes(root, df, scnd_frame))
    save_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()