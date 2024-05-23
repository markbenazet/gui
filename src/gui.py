import cv2
import datetime
import os
import tkinter as tk
from tkinter import messagebox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import numpy as np
import sys

# Add the setup directory to the system path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../setup'))

import config


class IconButton(tk.Canvas):
    def __init__(self, parent, width, height, image_path, command=None, toggle=False):
        super().__init__(parent, width=width, height=height, bd=0, highlightthickness=0, relief='ridge')
        
        self.command = command
        self.image_path = image_path
        self.width = width
        self.height = height
        self.toggle = toggle
        self.toggled = False

        self.image_original = Image.open(image_path).resize((width, height), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image_original)
        self.create_image(width / 2, height / 2, image=self.image, tags="img")
        
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        if self.toggle:
            if self.toggled:
                self.reset_scale()
            else:
                self.scale(0.9)
            self.toggled = not self.toggled
        else:
            self.scale(0.9)  # Decrease the button size slightly on click
            self.after(100, self.reset_scale)  # Reset size after 100 ms
        
        if self.command:
            self.command()

    def reset_scale(self):
        self.scale(1)  # Reset the scale

    def scale(self, factor):
        new_size = (int(self.width * factor), int(self.height * factor))
        resized_image = self.image_original.resize(new_size, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized_image)
        self.delete("img")
        self.create_image(self.width / 2, self.height / 2, image=self.image, tags="img")

class VideoRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Recorder")
        self.video_url = config.VIDEO_URL

        # Apply theme
        self.root.set_theme("radiance")

        try:
            self.cap = cv2.VideoCapture(self.video_url)
            if not self.cap.isOpened():
                raise Exception("Could not open video stream.")
        except Exception as e:
            logging.error("Error initializing video capture: %s", e)
            messagebox.showerror("Error", "Could not open video stream.")
            self.root.quit()

        self.is_recording = False
        self.out = None

        # Ensure the output directories exist
        self.videos_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), config.VIDEOS_DIR)
        self.pictures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), config.PICTURES_DIR)
        if not os.path.exists(self.videos_dir):
            os.makedirs(self.videos_dir)
        if not os.path.exists(self.pictures_dir):
            os.makedirs(self.pictures_dir)

        # Get absolute path for icons
        self.icons_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../icons')

        # Create UI components
        self.create_widgets()

        self.update()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=config.FRAME_WIDTH, height=config.FRAME_HEIGHT, bg='black')
        self.canvas.grid(row=0, column=0, columnspan=3, padx=10, pady=0)

        self.btn_record = IconButton(self.root, width=70, height=70, image_path=os.path.join(self.icons_dir, 'record.png'), command=self.toggle_recording, toggle=True)
        self.btn_record.grid(row=1, column=0, padx=20, pady=10)

        self.btn_capture = IconButton(self.root, width=70, height=70, image_path=os.path.join(self.icons_dir, 'capture.png'), command=self.capture_picture)
        self.btn_capture.grid(row=1, column=1, padx=20, pady=10)

        self.btn_quit = IconButton(self.root, width=70, height=70, image_path=os.path.join(self.icons_dir, 'exit.png'), command=self.quit)
        self.btn_quit.grid(row=1, column=2, padx=20, pady=10)

    def get_timestamp_filename(self, dir_path, extension):
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        return os.path.join(dir_path, f"{timestamp}.{extension}")

    def toggle_recording(self):
        try:
            if not self.is_recording:
                # Start recording with a timestamp filename
                filename = self.get_timestamp_filename(self.videos_dir, "avi")
                fourcc = cv2.VideoWriter_fourcc(*config.VIDEO_CODEC)
                self.out = cv2.VideoWriter(filename, fourcc, config.FRAME_RATE, (config.FRAME_WIDTH, config.FRAME_HEIGHT))
                self.is_recording = True
                print(f"Recording started: {filename}")
            else:
                # Stop recording
                self.out.release()
                self.is_recording = False
                print("Recording stopped.")
        except Exception as e:
            logging.error("Error during recording toggle: %s", e)
            messagebox.showerror("Error", "An error occurred during recording.")

    def capture_picture(self):
        try:
            ret, frame = self.cap.read()
            if ret:
                filename = self.get_timestamp_filename(self.pictures_dir, "png")
                cv2.imwrite(filename, frame)
                print(f"Picture captured: {filename}")
        except Exception as e:
            logging.error("Error capturing picture: %s", e)
            messagebox.showerror("Error", "An error occurred while capturing the picture.")


    def quit(self):
        self.cap.release()
        if self.is_recording:
            self.out.release()
        self.root.quit()

    def update(self):
        try:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (config.FRAME_WIDTH, config.FRAME_HEIGHT))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
                self.canvas.imgtk = imgtk

                if self.is_recording:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
                    self.out.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
        except Exception as e:
            logging.error("Error updating frame: %s", e)
            messagebox.showerror("Error", "An error occurred while updating the frame.")

        self.root.after(10, self.update)

if __name__ == "__main__":
    root = ThemedTk(theme="radiance")
    app = VideoRecorderApp(root)
    root.mainloop()
