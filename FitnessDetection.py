
import cv2 as cv
import mediapipe as mp
import numpy as np
import torch as pt
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import time
import sv_ttk

class Exercise:
    def __init__(self, name, repNumber, duration):
        self.name = name
        self.repNumber = repNumber
        self.duration = duration

class fitnessDetection:
    def __init__(self):
        self.exercises = []
        self.running = False

    def start_video(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        capture = cv.VideoCapture(1)

        if self.running:
            self.running = False
            if capture.isOpened:
                capture.release()
                cv.destroyAllWindows()
            start_button.config(text="Start Video")
            return

        self.running = True
        start_button.config(text = "Stop Recording")

        if not capture.isOpened():
            print("Cannot open camera")
            return
        
        previousTime = 0
   
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while self.running:
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
            
                currentTime = time.time()
                fps = 1 / (currentTime-previousTime)
                previousTime = currentTime

                cv.putText(image,str(int(fps))+ "FPS", (5,40), cv.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)

                #Extract key body landmarks if the landmark isnt null
                if  not results.pose_landmarks is None:
                    left_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
                    right_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
                    left_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
                    right_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]
                    left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
                    right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
                    left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                    right_shoulder= results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                else:
                    print("No landmarks detected")

                #calculate angles 

                #final adjustment to model

                #output

                # show ouput/video feed inside of tkinter window
                img = Image.fromarray(cv.cvtColor(image,cv.COLOR_BGR2RGB))
                imgtk = ImageTk.PhotoImage(image = img)
                
                image_label.imgtk = imgtk
                #configure photo image as the display image
                image_label.configure(image=imgtk)
                image_label.update()

                #exercise_log.insert(" ",tk.END,values = "Name: " + Exercise.name + "\nNumber of Reps: " + Exercise.repNumber + "\nTime Duration: " + Exercise.duration)

                

        capture.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    #create an instance of the fitnessDetection class
    detection = fitnessDetection()
    global image_label
    window = tk.Tk()
    window.minsize(1280, 800)
    window.title("Fitness Detection")

    #TKinter GUI widgets
    frame = ttk.Frame(window)
    frame.grid(row=0,column = 0, sticky = "nsew")

    left_frame =ttk.Frame(frame)
    left_frame.grid(row = 0, column =0)

    right_frame = ttk.Frame(frame)
    right_frame.grid(row = 0, column = 1)

    live_feed = ttk.LabelFrame(right_frame, text = "Live Feed")
    live_feed.grid(row = 0, column = 0, pady = 5, padx = 5)

    model_window = ttk.LabelFrame(right_frame, text = "3D Model")
    model_window.grid(row = 1, column = 0, pady = 5, padx = 5)

    
    image1 = Image.open("TemporaryImages/97148e50839746ab89f956c3b934cbb1.jpeg")
    image1 = image1.resize((360, 203), Image.LANCZOS)
    test = ImageTk.PhotoImage(image1)
    label1 = tk.Label(model_window,image=test)
    label1.image = test
    label1.grid(row=0, column=0, pady=5, padx=5)

    image_label = ttk.Label(live_feed)
    image_label.grid(row = 0, column = 0, pady = 5, padx = 5)

    button_group = ttk.Frame(left_frame)
    button_group.grid(row = 0,column=0)

    start_button = ttk.Button(button_group, text="Start Video",style = "Toggle.TButton", command=detection.start_video)
    start_button.grid(row =0, column = 0, pady = 10, padx = 5)

    pause_button = ttk.Button(button_group, text = "Pause Program", style = "Toggle.TButton")
    pause_button.grid(row=0, column = 1, pady = 10, padx = 5)

    restart_button = ttk.Button(button_group, text = "Restart Tracking", style = "Acccent.TButton")
    restart_button.grid(row = 0, column =2, pady = 10, padx = 5)

    Calorie_label = ttk.LabelFrame(left_frame, text = "Calories Burned")
    Calorie_label.grid(row= 2, column = 0,pady = 5, padx = 5 )

    Calorie_Data = ttk.Label(Calorie_label, text = "Total Calories Burned:", width=75)
    Calorie_Data.grid(row =0, column = 0, pady = 5, padx = 5)


    exercise_log = ttk.Treeview(left_frame,height = 25)
    exercise_log.grid(row = 1, column = 0, pady=5, padx=20)
    exercise_log.heading("#0", text = "Exercise Log")
    exercise_log.column("#0", width=600)

   

    sv_ttk.set_theme("dark")
    window.mainloop()

