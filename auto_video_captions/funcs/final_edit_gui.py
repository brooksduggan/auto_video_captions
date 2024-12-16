import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import pygame
import os
import threading
import queue

class VideoScrubberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Scrubber")
        
        self.video_path = None
        self.video_capture = None
        self.frames = []
        self.thumbnail_images = []
        self.frame_count = 0
        self.original_width, self.original_height = 320, 180
        self.current_frame_idx = 0  # Track current frame index
        self.is_playing = False
        self.current_image = None  # Store a reference to the current image

        # Default aspect ratio (e.g., 16:9)
        self.aspect_ratio_width = 9
        self.aspect_ratio_height = 16
        
        # Default output size (calculated based on aspect ratio)
        self.output_width = self.original_width
        self.output_height = self.original_height
        
        # Initialize pygame mixer for audio
        pygame.mixer.init()

        # Queue for communication between threads
        self.frame_queue = queue.Queue()

        self.create_widgets()

    def create_widgets(self):
        # Button to load video
        self.load_button = tk.Button(self.root, text="Open .mkv Video", command=self.load_video)
        self.load_button.pack(pady=10, side='top')

        # Canvas to display the grid of thumbnails
        self.canvas = tk.Canvas(self.root, width=self.original_width, height=self.original_height)
        self.canvas.pack(pady=10)

        # Input for aspect ratio (e.g., 16:9)
        self.aspect_ratio_label = tk.Label(self.root, text="Aspect Ratio (Width:Height):")
        self.aspect_ratio_label.pack(pady=5)
        self.aspect_ratio_entry = tk.Entry(self.root)
        self.aspect_ratio_entry.insert(0, f"{self.aspect_ratio_width}:{self.aspect_ratio_height}")  # Default aspect ratio
        self.aspect_ratio_entry.pack(pady=5)

        # Input for output size (width or height)
        self.size_label = tk.Label(self.root, text="Enter Desired Width (or Height):")
        self.size_label.pack(pady=5)
        self.size_entry = tk.Entry(self.root)
        self.size_entry.insert(0, str(self.output_width))  # Set default width
        self.size_entry.pack(pady=5)

        # Apply button to update output size
        self.apply_button = tk.Button(self.root, text="Apply Aspect Ratio and Size", command=self.apply_output_size)
        self.apply_button.pack(pady=10)

        # Play and Pause Buttons
        self.play_button = tk.Button(self.root, text="Play", command=self.play_video)
        self.play_button.pack(side="left", padx=10)
        
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_video)
        self.pause_button.pack(side="left", padx=10)

        # Scale to scrub through the video
        self.scale = tk.Scale(self.root, from_=0, to=100, orient="horizontal", label="Scrub", command=self.update_frame)
        self.scale.pack(fill="x", padx=20, side='bottom')
        # Bind the event when the user releases the slider
        self.scale.bind("<ButtonRelease-1>", self.stop_audio_on_slider_release)

    def apply_output_size(self):
        # Get aspect ratio from the input field (e.g., 16:9)
        aspect_ratio_str = self.aspect_ratio_entry.get()
        try:
            width, height = map(int, aspect_ratio_str.split(":"))
            if width <= 0 or height <= 0:
                raise ValueError("Aspect ratio values must be positive integers.")
            self.aspect_ratio_width = width
            self.aspect_ratio_height = height

            # Get width or height from the input field
            size = int(self.size_entry.get())
            if size <= 0:
                raise ValueError("Size must be a positive integer.")

            # Calculate the other dimension based on the aspect ratio
            if self.aspect_ratio_width / self.aspect_ratio_height >= 1:
                # Calculate based on width
                self.output_width = size
                self.output_height = int(self.output_width * self.aspect_ratio_height / self.aspect_ratio_width)
            else:
                # Calculate based on height
                self.output_height = size
                self.output_width = int(self.output_height * self.aspect_ratio_width / self.aspect_ratio_height)

            # Update canvas size
            self.canvas.config(width=self.output_width, height=self.output_height)

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please enter valid values for aspect ratio and size.\nError: {e}")
    
    def load_video(self):
        # Open file dialog to choose a .mkv file
        self.video_path = filedialog.askopenfilename(filetypes=[("MKV Files", "*.mkv")])
        if self.video_path:
            # Load video
            self.video_capture = cv2.VideoCapture(self.video_path)
            self.frame_count = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.thumbnail_images = []
            self.frames = []

            # Start frame extraction in a background thread
            threading.Thread(target=self.extract_thumbnails, daemon=True).start()

            # Enable the scale widget
            self.scale.config(to=self.frame_count - 1, state="normal")

            # Load and pause audio (don't play automatically)
            self.load_audio()

    def extract_thumbnails(self):

        # After extracting thumbnails, update the UI on the main thread
        self.root.after(0, self.display_thumbnails)

    def display_thumbnails(self):
        # Display the thumbnails in a grid
        
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            image = image.resize((self.output_width, self.output_height))  # Resize based on aspect ratio
            photo = ImageTk.PhotoImage(image)

            # Clear previous frame
            self.canvas.delete("all")
            
            # Display the current frame
            self.canvas.create_image(0, 0, anchor="nw", image=photo)

            # Store reference to the image
            self.current_image = photo

    def load_audio(self):
        # Load the audio file associated with the video (if available)
        audio_file = self.video_path.replace(".mkv", ".mp3")
        if not os.path.exists(audio_file):
            messagebox.showerror("Error", "Audio file not found. Ensure the video has an associated audio track.")
            return
        
        # Load the audio into pygame, but don't start it immediately
        pygame.mixer.music.load(audio_file)
        self.audio_length = self.get_audio_length(audio_file)  # Get the length of the audio file
        pygame.mixer.music.set_volume(1.0)  # Set volume to 100%

    def get_audio_length(self, audio_file):
        """Return the length of the audio file in seconds."""
        sound = pygame.mixer.Sound(audio_file)
        return sound.get_length()

    def update_frame(self, value):
        # Stop video from continuously updating
        if self.is_playing and not self.play:
            self.is_playing = False
            return

        # Update video frame when scale is moved
        value = int(value)
        self.current_frame_idx = value
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, value)
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            image = image.resize((self.output_width, self.output_height))  # Resize based on aspect ratio
            photo = ImageTk.PhotoImage(image)

            # Clear previous frame
            self.canvas.delete("all")
            
            # Display the current frame
            self.canvas.create_image(0, 0, anchor="nw", image=photo)

            # Store reference to the image
            self.current_image = photo

            # Update the scale position
            self.scale.set(value)

            # Sync the audio with the video
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(loops=0, start=value / self.frame_count * self.audio_length)

            pygame.mixer.music.set_pos(value / self.frame_count * self.audio_length)
            pygame.mixer.music.pause()

    def stop_audio_on_slider_release(self, event):
        # Stop the audio when the slider is released
        pygame.mixer.music.stop()

    def play_video(self):
        # Start video and audio playback from the current position
        self.play = True
        if not self.is_playing:
            self.is_playing = True
            self.play_frame(self.current_frame_idx)

    def pause_video(self):
        # Pause video and audio playback
        self.play = False
        self.is_playing = False
        pygame.mixer.music.pause()

    def play_frame(self, frame_idx):
        # Play frames sequentially with a short delay
        if not self.is_playing or frame_idx >= self.frame_count:
            return

        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            image = image.resize((self.output_width, self.output_height))  # Resize based on aspect ratio
            photo = ImageTk.PhotoImage(image)

            # Clear previous frame
            self.canvas.delete("all")
            
            # Display the current frame
            self.canvas.create_image(0, 0, anchor="nw", image=photo)

            # Store reference to the image
            self.current_image = photo

            # Update the scale position
            self.scale.set(frame_idx)

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(loops=0, start=round(frame_idx / self.frame_count * self.audio_length, 3))
            
            # Call this method again after a short delay (for smooth playback)
            if self.is_playing:
                self.root.after(50, self.play_frame, frame_idx + 1)  # Update every 50 ms

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoScrubberApp(root)
    root.mainloop()
