import tkinter as tk
from tkinter import filedialog
import pandas as pd
from config import *


class mainGUIs:

    def _load_csv(self, file_path):
        df = pd.read_csv(file_path)
        return df

    def _save_csv(self, root, df, file_path):
        df.to_csv(file_path, index=False)
        root.destroy()

    def _create_table(self, df, frame):
        df = df[['full_text', 'segment_id']].drop_duplicates()
        max_length = df['full_text'].str.len().max()
        segment_id = tk.Label(frame, text='ID', font=("Arial", 16, "bold"), bg='SlateGray4')
        segment_id.grid(row=0, column=0, sticky='w')

        full_text = tk.Label(frame, text='Transcription', font=("Arial", 16, "bold"), bg='SlateGray4')
        full_text.grid(row=0, column=1, sticky='w')
        for index, row in df.iterrows():
            segment_id = tk.Label(frame, text=row['segment_id'].split("_")[1], bg='SlateGray4')
            # segment_id.insert(0, row['segment_id'])
            segment_id.grid(row=index+1, column=0, sticky='w')

            full_text = tk.Entry(frame, width=max_length, bg='azure')
            full_text.insert(0, row['full_text'])
            full_text.grid(row=index+1, column=1)

    def _update_check(self, df):

        for i, r in df.iterrows():
            start = r['word_id']//word_threshold*word_threshold
            end = ((r['word_id']//word_threshold)+1)*word_threshold
            word_list = r['full_text'].lstrip().upper().split()
            new_sub = ' '.join(word_list[start:end])
            if r['sub_phrase'] != new_sub:
                df.loc[df['sub_phrase'] == r['sub_phrase'], 'sub_phrase'] = new_sub
                df.loc[(df['word_id'] == r['word_id']) & (df['phrase_id'] == r['phrase_id']), 'word_used'] = word_list[r['word_id']]

        return df


    def _save_changes(self, root, df, frame):
        update_df = df[['full_text', 'segment_id']].drop_duplicates()
        for index, row in update_df.iterrows():
            segment_id = frame.grid_slaves(row=index, column=0)
            full_text = frame.grid_slaves(row=index, column=1)

            df.loc[df['segment_id'] == segment_id[0].get(), 'full_text'] = full_text[0].get()

        final_df = self._update_check(df)

        self._save_csv(root=root, df=final_df, file_path=new_output)  # Replace 'updated_file.csv' with your desired output file

    def _get_proj_path(self):
        folder_path = filedialog.askdirectory()
        self.proj_entry.config(state='normal')
        self.proj_entry.delete(0, tk.END)
        self.proj_entry.insert(0, folder_path)
        len_file = len(folder_path)
        self.proj_entry.config(state='readonly', readonlybackground='grey50', width=len_file)


    def _get_vid_path(self):
        filetypes = (
            ('Video files', '*.mp4 *.avi *.mkv *.mov'),  # Add more video formats if needed
            ('All files', '*.*')
        )
        video_path = filedialog.askopenfilenames(
            title="Select a video file",
            filetypes=filetypes
        )
        self.vid_entry.config(state='normal')
        self.vid_entry.delete(0, tk.END)
        self.vid_entry.insert(0, video_path[0])
        len_path = len(video_path[0])
        self.vid_entry.config(state='readonly', readonlybackground='grey50', width=len_path)

    def video_loader_gui(self):

        root = tk.Tk()
        root.title("Video Editor - Choose Video")
        root.configure(bg='SlateGray4')

        frame = tk.Frame(root)
        frame.configure(bg='SlateGray4')
        frame.pack(fill='both', expand=1)
        directions_title = tk.Label(frame, text='Directions', font=("Arial", 25, "bold"), bg='SlateGray4')
        directions_title.pack()
        
        directions_desc = tk.Label(frame, text="""Select (1) a folder path you would like to save your Project,\n(2) which video file you want to transcribe and add captions to.""", font=("Arial", 14), bg='SlateGray4')
        directions_desc.pack()

        my_canvas = tk.Canvas(frame)
        my_canvas.configure(bg='SlateGray4')
        my_canvas.pack(side='left', fill='both', expand=1)

        scrollbar = tk.Scrollbar(frame, orient='vertical', command=my_canvas.yview)
        scrollbar.pack( side = "right", fill="y" )

        my_canvas.configure(yscrollcommand=scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))

        scnd_frame = tk.Frame(my_canvas)
        scnd_frame.configure(bg='SlateGray4')

        my_canvas.create_window((0,0), window=scnd_frame, anchor='nw')

        proj_name_title = tk.Label(scnd_frame, text='Project Name:', font=("Arial", 12, "bold"), bg='SlateGray4')
        proj_name_title.grid(row=0, column=0)
        proj_name = tk.Entry(scnd_frame, width=50, bg='azure')
        proj_name.grid(row=0, column=1)

        proj_path_title = tk.Label(scnd_frame, text='Project Path:', font=("Arial", 12, "bold"), bg='SlateGray4')
        proj_path_title.grid(row=1, column=0)
        self.proj_entry = tk.Entry(scnd_frame, width=50, state='readonly', readonlybackground='grey50')
        self.proj_entry.grid(row=1, column=1)
        proj_path = tk.Button(scnd_frame, text="Output Path",width=10, height=2, bg="grey", fg="white", command=lambda: self._get_proj_path())
        proj_path.grid(row=1, column=2, padx=20, pady=3)

        vid_path_title = tk.Label(scnd_frame, text='Video Path:', font=("Arial", 12, "bold"), bg='SlateGray4')
        vid_path_title.grid(row=2, column=0)
        self.vid_entry = tk.Entry(scnd_frame, width=50, state="readonly", readonlybackground='grey50')
        self.vid_entry.grid(row=2, column=1)
        video_path = tk.Button(scnd_frame, text="Choose Video",width=10, height=2, bg="grey", fg="white", command=lambda: self._get_vid_path())
        video_path.grid(row=2, column=2, padx=20, pady=3)

        run_button = tk.Button(root, text="Transcribe",width=10, height=2, bg="forest green", fg="white", command=lambda: transcribe_video(root, ))
        run_button.pack(side='right',padx=20, pady=3)

        width= root.winfo_screenwidth() 
        height= root.winfo_screenheight()
        #setting tkinter window size
        root.geometry("%dx%d" % (width, height))
        root.title("Transcription Editor")
        root.state('zoomed')

        root.mainloop()

    def transcription_editor_gui(self):
        file_path = test_csv  # Replace with your actual file path
        df = self._load_csv(file_path)

        root = tk.Tk()
        root.title("CSV Editor")
        root.configure(bg='SlateGray4')

        frame = tk.Frame(root)
        frame.configure(bg='SlateGray4')
        frame.pack(fill='both', expand=1)
        directions_title = tk.Label(frame, text='Directions', font=("Arial", 25, "bold"), bg='SlateGray4')
        directions_title.pack()
        
        directions_desc = tk.Label(frame, text="""Make any edits, if any, to the below transcription (including punctuation) - this will ensure accurate captions.\nCaptions *will* be automatically converted to all UPPERCASE.\nIf no changes, select the 'No Changes' button.""", font=("Arial", 14), bg='SlateGray4')
        directions_desc.pack()

        my_canvas = tk.Canvas(frame)
        my_canvas.configure(bg='SlateGray4')
        my_canvas.pack(side='left', fill='both', expand=1)

        scrollbar = tk.Scrollbar(frame, orient='vertical', command=my_canvas.yview)
        scrollbar.pack( side = "right", fill="y" )

        my_canvas.configure(yscrollcommand=scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))

        scnd_frame = tk.Frame(my_canvas)
        scnd_frame.configure(bg='SlateGray4')

        my_canvas.create_window((0,0), window=scnd_frame, anchor='nw')

        self._create_table(df, scnd_frame)

        save_button = tk.Button(root, text="Save Changes",width=10, height=2, bg="forest green", fg="white", command=lambda: self._save_changes(root, df, scnd_frame))
        save_button.pack(side='right',padx=20, pady=3)
        no_change_button = tk.Button(root, text="No Changes",width=10, height=2, bg="LightBlue3", fg="gray25", command=lambda: root.destroy())
        no_change_button.pack(side='right', padx=20, pady=3)

        width= root.winfo_screenwidth() 
        height= root.winfo_screenheight()
        #setting tkinter window size
        root.geometry("%dx%d" % (width, height))
        root.title("Transcription Editor")
        root.state('zoomed')

        root.mainloop()

if __name__ == "__main__":
    m = mainGUIs()
    m.video_loader_gui()
    # transcription_editor_gui()