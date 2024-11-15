import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
    if file_path:
        print(file_path)
        image = Image.open(file_path)
        w, h = image.size

        # Scale the image to fit the frame
        image = image.resize((int(w*.3), int(h*.3)))

        photo = ImageTk.PhotoImage(image)

        image_label.config(image=photo)
        image_label.image = photo

# Create the main window
root = tk.Tk()
root.title("Image Viewer")

# Set the window to full screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Create a frame for parameter input
parameter_frame = tk.Frame(root)
parameter_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add parameter input widgets here (e.g., labels, entry fields, buttons)
# ...

# Create a frame for image display
image_frame = tk.Frame(root, bg="black")
image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create a label to display the image
image_label = tk.Label(image_frame, bg="black")
image_label.pack(fill=tk.BOTH, expand=True)

# Create a button to open a file
open_button = tk.Button(parameter_frame, text="Open Image", command=open_file)
open_button.pack(pady=10)

root.mainloop()