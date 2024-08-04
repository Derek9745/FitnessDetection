
import cv2 as cv
import mediapipe as mp
import numpy as np
import torch as pt
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
capture = cv.VideoCapture(1)

def start_video():
    if not capture.isOpened():
        print("Cannot open camera")
        return

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            #capture video feed
            ret, frame = capture.read()
    
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            # Convert the frame colors from BGR to RGB
            image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Convert the image colors back from RGB to BGR
            image.flags.writeable = True
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

            # Draw the pose annotation on the image
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # show ouput/video feed inside of tkinter window
            img = Image.fromarray(cv.cvtColor(image,cv.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image = img)
            

            image_label.imgtk = imgtk
            #configure photo image as the display image
            image_label.configure(image=imgtk)
            image_label.update()
          
            ##cv.imshow("video", image)

            #if q is pressed, exit video feed
            if cv.waitKey(1) == ord('q'):

                break

    capture.release()
    cv.destroyAllWindows()

def start_application():
    global image_label
    window = tk.Tk()
    window.minsize(1000, 600)
    window.title("Fitness Detection")
    frame = ttk.Frame(window)
    
    # Create a label in the frame
    frame.pack()
    image_label = ttk.Label(frame)
    image_label.pack(anchor = "center", pady = 15)
    start_button = ttk.Button(frame, text="Start Video", command=start_video)
    start_button.pack(pady=20)
    window.mainloop()

if __name__ == "__main__":
    start_application()
