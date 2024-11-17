import tkinter as tk
import pandas as pd

def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def save_csv(df, file_path):
    df.to_csv(file_path, index=False)

def create_table(df, frame):
    for index, row in df.iterrows():
        sub_phrase = tk.Entry(frame)
        sub_phrase.insert(0, row['sub_phrase'])
        sub_phrase.grid(row=index, column=0)

        start_frame_entry = tk.Entry(frame)
        start_frame_entry.insert(0, row['word_frame_start'])
        start_frame_entry.grid(row=index, column=1)

        end_frame_entry = tk.Entry(frame)
        end_frame_entry.insert(0, row['word_frame_end'])
        end_frame_entry.grid(row=index, column=2)

def save_changes(df, frame):
    for index, row in df.iterrows():
        sub_phrase = frame.grid_slaves(row=index, column=0)
        start_frame_entry = frame.grid_slaves(row=index, column=1)
        end_frame_entry = frame.grid_slaves(row=index, column=2)

        df.at[index, 'sub_phrase'] = sub_phrase
        df.at[index, 'start_frame'] = int(start_frame_entry.get())
        df.at[index, 'end_frame'] = int(end_frame_entry.get())

    save_csv(df, 'updated_file.csv')  # Replace 'updated_file.csv' with your desired output file

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

    save_button = tk.Button(root, text="Save Changes", command=lambda: save_changes(df, scnd_frame))
    save_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()