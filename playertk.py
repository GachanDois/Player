import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter import filedialog

class VideoPlayer:
    def __init__(self, master, x, y, width, height):
        self.master = master
        self.video_file = None
        self.video_capture = None
        self.video_width = None
        self.video_height = None
        self.canvas = tk.Canvas(self.master, width=width, height=height)
        self.canvas.place(x=x, y=y)

    def play(self):
        if self.video_capture is not None:
            ret, frame = self.video_capture.read()
            if ret:
                # Resize the frame to fit the canvas while maintaining aspect ratio
                aspect_ratio = self.video_width / self.video_height
                canvas_width = self.canvas.winfo_width()
                canvas_height = int(canvas_width / aspect_ratio)
                if canvas_height > self.canvas.winfo_height():
                    canvas_height = self.canvas.winfo_height()
                    canvas_width = int(canvas_height * aspect_ratio)

                # Ensure the output size is not too small
                if canvas_width < 1 or canvas_height < 1:
                    return

                try:
                    frame = cv2.resize(frame, (canvas_width, canvas_height), interpolation=cv2.INTER_AREA)
                except cv2.error as e:
                    print(f"Error resizing frame: {e}")
                    return

                # Convert the frame to RGB format and create an ImageTk PhotoImage
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                photo = ImageTk.PhotoImage(image=image)

                # Display the image on the canvas
                self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)

                # Schedule the next frame to be read after a delay of 30 milliseconds
                self.master.after(30, self.play)
            else:
                # Release the video capture object when the video is finished
                self.video_capture.release()

    def select_video(self):
        # Open file selector dialog to choose video file
        video_file = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
        if video_file:
            # Release the current video capture and set new video file
            if self.video_capture is not None:
                self.video_capture.release()
            self.video_file = video_file
            self.video_capture = cv2.VideoCapture(video_file)
            self.video_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.video_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.play()

# Create the main application window
root = tk.Tk()
root.title("Multi-Video Player")
root.geometry("800x600")

# Define the positions and sizes for each video display
video_positions = [(0, 0, 400, 300), (400, 0, 400, 300), (0, 300, 400, 300), (400, 300, 400, 300)]

# Create the VideoPlayer instances for each video display
players = []
for i, video_position in enumerate(video_positions):
    x, y, width, height = video_position
    player = VideoPlayer(root, x, y, width, height)
    players.append(player)

# Button to select videos
select_button = tk.Button(root, text="Select Videos", command=lambda: [player.select_video() for player in players])
select_button.pack()

# Run the main event loop
root.mainloop()
