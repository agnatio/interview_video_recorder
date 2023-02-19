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

        # still not sure if this button is needed
        # self.save_button = tk.Button(self.root, text="Save", command=self.save_file, state=tk.DISABLED)
        # self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

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


# рабочий вариант

# import cv2 as cv
# import time
# import tkinter as tk
# from tkinter import messagebox
# from PIL import ImageTk, Image

# class VideoRecorder:
#     def __init__(self):
#         self.cap = cv.VideoCapture(0)
#         self.fourcc = cv.VideoWriter_fourcc(*'XVID')
#         self.out = cv.VideoWriter('output.avi', self.fourcc, 20.0, (640, 480))
#         self.recording = False

#         self.root = tk.Tk()
#         self.root.title("Video Recorder")

#         self.start_button = tk.Button(self.root, text="Start", command=self.start_recording)
#         self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

#         self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_recording, state=tk.DISABLED)
#         self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)

#         self.video_label = tk.Label(self.root)
#         self.video_label.config(image=tk.PhotoImage(width=640, height=480))
#         self.video_label.pack(side=tk.TOP)

#         self.root.mainloop()

#     def start_recording(self):

#         self.recording = True
#         self.start_button.config(state=tk.DISABLED)
#         self.stop_button.config(state=tk.NORMAL)

#         while self.recording:
#             ret, frame = self.cap.read()
#             if ret == True:
#                 self.out.write(frame)

#                 # Convert the video frame to a PIL image and display it in the Tkinter window
#                 frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
#                 # set frame size 480x640
#                 frame_rgb = cv.resize(frame_rgb, (640, 480))
#                 frame_pil = Image.fromarray(frame_rgb)
#                 frame_tk = ImageTk.PhotoImage(frame_pil)
#                 self.video_label.config(image=frame_tk)
#                 self.video_label.image = frame_tk

#                 self.root.update()
#             else:
#                 break

#     def stop_recording(self):
#         self.recording = False
#         self.start_button.config(state=tk.NORMAL)
#         self.stop_button.config(state=tk.DISABLED)

#         self.cap.release()
#         self.out.release()
#         cv.destroyAllWindows()

#         # Display a message box to indicate that the recording has stopped
#         tk.messagebox.showinfo("Recording Stopped", "The video has been saved to output.avi")
#         self.root.destroy()


# if __name__ == '__main__':
#     VideoRecorder()



# неплохо работает из окошка
# import cv2 as cv
# import time

# cap = cv.VideoCapture(0)
# fourcc = cv.VideoWriter_fourcc(*'XVID')
# out = cv.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# # Create a new window to display the recording process
# cv.namedWindow("Recording", cv.WINDOW_NORMAL)

# # Record for 5 seconds
# start_time = time.time()
# while(time.time() - start_time < 5):
#     ret, frame = cap.read()
#     if ret == True:
#         out.write(frame)
#         cv.imshow('Recording', frame) # Display the video frames in the new window
#         cv.waitKey(1) # Wait for a key press to refresh the window
#     else:
#         break

# cap.release()
# out.release()
# cv.destroyAllWindows()





# что то пишет, но непонятно что
# import cv2 as cv

# import time

# cap = cv.VideoCapture(0)
# fourcc = cv.VideoWriter_fourcc(*'XVID')
# out = cv.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# # Record for 5 seconds
# start_time = time.time()
# while(time.time() - start_time < 5):
#     ret, frame = cap.read()
#     if ret == True:
#         # frame = cv.flip(frame, 1)
#         out.write(frame)
#         cv.imshow('frame', frame)
#     else:
#         break

# cap.release()
# out.release()
# cv.destroyAllWindows()


# """
# capture laptop camera and exit with q"""
# cap = cv.VideoCapture(0)
# while True:
#     ret, frame = cap.read()
#     cv.imshow('frame', frame)
#     if cv.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv.destroyAllWindows()

# """
# record 20 seconds of video from laptop camera and exit with q"""
# cap = cv.VideoCapture(0)
# fourcc = cv.VideoWriter_fourcc(*'XVID')
# out = cv.VideoWriter('output.avi', fourcc, 5.0, (640, 480))
# while cap.isOpened():
#     ret, frame = cap.read()
#     if ret == True:
#         frame = cv.flip(frame, 1)
#         out.write(frame)
#         cv.imshow('frame', frame)
#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break
#     else:
#         break
# cap.release()
# out.release()
# cv.destroyAllWindows()
