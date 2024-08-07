
import cv2 as cv
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import time
import sv_ttk
from Panda_app import Panda3DApp 


class Exercise:
    def __init__(self, name, repNumber, duration):
        self.name = name
        self.repNumber = repNumber
        self.duration = duration

class fitnessDetection:
    def __init__(self):
        self.exercises = []
        self.running = False

    def calculateAngle(a,b,c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        if angle>180.0:
            angle = 360-angle
        return angle


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
                    left_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
                    left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
                
                    #calculate angle
                    angle = detection.calculateAngle(left_knee, left_ankle,left_hip)
                    if angle> 160:
                        stage = "down"
                    if angle<30 and stage == "down":
                        counter+=1
                        exercise_log.insert(" ",tk.END,values = "Name: Squat" + "\nNumber of Reps: " + counter + "\nTime Duration: ")
                else:
                    print("No landmarks detected")

                # show ouput/video feed inside of tkinter window
                img = Image.fromarray(cv.cvtColor(image,cv.COLOR_BGR2RGB))
                imgtk = ImageTk.PhotoImage(image = img)
                
                image_label.imgtk = imgtk
                #configure photo image as the display image
                image_label.configure(image=imgtk)
                image_label.update()
   
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

    #image1 = Image.open("TemporaryImages/97148e50839746ab89f956c3b934cbb1.jpeg")
    #image1 = image1.resize((360, 203), Image.LANCZOS)
    #test = ImageTk.PhotoImage(image1)

    panda_frame = tk.Frame(model_window, width=640, height=480)
    panda_frame.grid(row=0, column=0, pady=5, padx=5)
    panda_window = Panda3DApp(panda_frame)


   

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

