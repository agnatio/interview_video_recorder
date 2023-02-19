# ready video recorder

import cv2 as cv
import time
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

class VideoRecorder:
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        self.fourcc = cv.VideoWriter_fourcc(*'XVID')
        self.out = None
        self.recording = False

        self.root = tk.Tk()
        self.root.title("Video Recorder")

        self.start_button = tk.Button(self.root, text="Start", command=self.start_recording)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.video_label = tk.Label(self.root)
        self.video_label.pack(side=tk.TOP)

        self.root.mainloop()

    def start_recording(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Ask the user for the output file name and location
        file_path = filedialog.asksaveasfilename(defaultextension='.avi', filetypes=[('AVI files', '*.avi')])
        if file_path:
            self.out = cv.VideoWriter(file_path, self.fourcc, 20.0, (640, 480))

        # Display countdown timer for 3 seconds
        for i in range(3, 0, -1):
            font = cv.FONT_HERSHEY_SIMPLEX

            bottomLeftCornerOfText = (280, 240)
            fontScale = 2
            fontColor = (0, 0, 255)
            lineType = 2
            ret, frame = self.cap.read()
            frame = cv.flip(frame, 1)
            cv.putText(frame, str(i), bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            frame_tk = ImageTk.PhotoImage(frame_pil)
            self.video_label.config(image=frame_tk)
            self.video_label.image = frame_tk
            self.root.update()
            time.sleep(1)

        while self.recording:
            ret, frame = self.cap.read()
            if ret == True:
                self.out.write(frame)

                # Convert the video frame to a PIL image and display it in the Tkinter window
                frame = cv.flip(frame, 1)

                frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                frame_pil = Image.fromarray(frame_rgb)
                frame_tk = ImageTk.PhotoImage(frame_pil)
                self.video_label.config(image=frame_tk)
                self.video_label.image = frame_tk

                self.root.update()
            else:
                break

        # Enable the Save button when recording is stopped
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state=tk.NORMAL)

    def save_file(self):
        # Ask the user for the output file name and location
        file_path = filedialog.asksaveasfilename(defaultextension='.avi', filetypes=[('AVI files', '*.avi')])
        if file_path:
            # Release the camera and video file and close the display window
            self.cap.release()
            self.out.release()
            cv.destroyAllWindows()

            # Copy the video file to the user-specified location
            import shutil
            shutil.copy('output.avi', file_path)

            # Display a message box to indicate that the file has been saved
            tk.messagebox.showinfo("File Saved", "The video has been saved to {}".format(file_path))

            # Reset the UI to allow starting a new recording
            self.out = None
            self.save_button.config(state=tk.DISABLED)
            self.start_button.config(state=tk.NORMAL)

if __name__ == '__main__':
    VideoRecorder()


