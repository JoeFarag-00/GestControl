import customtkinter
import os
import threading
from tkinter import Tk
from tkinter import messagebox
from tkinter import filedialog
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('green')
import re
import cv2
from tkinter import Label, Text, Button, Menu
import random
from PIL import Image
from tkinter_webcam import webcam
import time
import sys
import socket
import mediapipe as mp
import pyautogui
import numpy as np
from Gest import *

Main = customtkinter.CTk()

class MainGUI:
    def __init__(self):
        self.Main = Main
        self.start_model = False
        self.Get_Fist_Stat = Fist_Recognizer()
        self.Get_Pinch_Stat = Pinch_Recognizer()
        self.Get_Peace_Stat = Peace_Detector()


       
    @staticmethod
    def DestroyAll():
        widgets = Main.winfo_children()
        for widget in widgets:
            widget.destroy()

    def Continue(self):
        self.DestroyAll()
        self.Get_Dashboard()
        
    def Exit(self):
        os._exit(0)


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def Get_Dashboard(self):
        self.DestroyAll()
        self.bots = None
        self.users = None
        self.sent_message = None
        self.received_message = None
        self.name = "Nurse"
        self.Fist_Stat = None
        self.message_counter = 1
        self.chat_counter = 2
        self.Main.resizable(width=False, height=False)
        self.Main.title("Dashboard")
        self.Main.geometry(f"{1100}x{510}")
        self.Main.grid_columnconfigure(1, weight=1)
        self.app_logo = customtkinter.CTkImage(light_image=Image.open("Assets/logo.png"), size=(100, 100))
        self.sidebar_frame = customtkinter.CTkFrame(self.Main, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo = customtkinter.CTkLabel(self.sidebar_frame, image=self.app_logo, text="", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="GestControl", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=20)
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_options = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_options.grid(row=5, column=0, padx=20, pady=(10, 10))
        self.exit_button = customtkinter.CTkButton(self.sidebar_frame, text="Exit", hover_color="Red", command=self.Exit)
        self.exit_button.grid(row=6, column=0, padx=20, pady=10)
        self.tabview = customtkinter.CTkTabview(master=self.Main, width=250, height=490)
        self.tabview.grid(row=1, column=1, columnspan=2, padx=(20, 10), pady=(10, 0), sticky="nsew")
        self.tabview.add("Available Gestures")
        self.tabview.set("Available Gestures")
        self.Apply_Gest_Profiles()

            
    def Apply_Gest_Profiles(self):
        
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Available Gestures"), width=845,height=430)
        self.scrollable_frame.grid(row=0, column=0, padx=(5, 0), pady=(5, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        
        #----------------------------------------
        
        self.Gest1Frame = customtkinter.CTkFrame(self.scrollable_frame, corner_radius=20, fg_color="#628680",border_width=5, border_color="black",width=250,height=300)
        self.Gest1Frame.grid(row=0, column=0,pady=20,padx=10)

        self.Gest1 = customtkinter.CTkImage(Image.open(self.current_path + "\Assets\pinch.png"),size=(140, 150))
        self.Gest1_bg = customtkinter.CTkLabel(self.Gest1Frame, image=self.Gest1,text = "")
        self.Gest1_bg.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        self.Gest1_LBl = customtkinter.CTkLabel(self.Gest1Frame,text = f"Pinch Gesture", text_color = "white",font=("System", 23, "bold"))
        self.Gest1_LBl.grid(row=1, column=0, padx=20, pady=(20, 20))
        
        self.Shortcut1 = customtkinter.CTkEntry(self.Gest1Frame, width=100, placeholder_text="Enter Shortcut")
        self.Shortcut1.grid(row=2, column=0, padx=30, pady=(0, 15))
        
        self.Shortcut1_Btn = customtkinter.CTkButton(self.Gest1Frame,hover_color="orange", text="Set")
        self.Shortcut1_Btn.grid(row=3, column=0, padx=20, pady=(0, 20))

        #-----------------------------
        
        self.Gest2Frame = customtkinter.CTkFrame(self.scrollable_frame, corner_radius=20, fg_color="#628680",border_width=5, border_color="black",width=250,height=300)
        self.Gest2Frame.grid(row=0, column=1,pady=20,padx=10)

        self.Gest2 = customtkinter.CTkImage(Image.open(self.current_path + "/Assets/fist.png"),size=(160, 160))
        self.Gest2_bg = customtkinter.CTkLabel(self.Gest2Frame, image=self.Gest2,text = "")
        self.Gest2_bg.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        self.Gest2_LBl = customtkinter.CTkLabel(self.Gest2Frame,text = f"Fist Gesture", text_color = "white",font=("System", 23, "bold"))
        self.Gest2_LBl.grid(row=1, column=0, padx=20, pady=(20, 20))
        
        self.Shortcut2 = customtkinter.CTkEntry(self.Gest2Frame, width=100, placeholder_text="Enter Shortcut")
        self.Shortcut2.grid(row=2, column=0, padx=30, pady=(0, 15))
        
        self.Shortcut2_Btn = customtkinter.CTkButton(self.Gest2Frame,hover_color="orange", text="Set")
        self.Shortcut2_Btn.grid(row=3, column=0, padx=20, pady=(0, 20))
        
        # #----------------------------------------
        self.Gest3Frame = customtkinter.CTkFrame(self.scrollable_frame, corner_radius=20, fg_color="#628680",border_width=5, border_color="black",width=250,height=300)
        self.Gest3Frame.grid(row=0, column=2,pady=20, padx=50)

        self.Gest3 = customtkinter.CTkImage(Image.open(self.current_path + "\Assets\peace.png"),size=(150, 150))
        self.Gest3_bg = customtkinter.CTkLabel(self.Gest3Frame, image=self.Gest3,text = "")
        self.Gest3_bg.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        self.Gest3_LBl = customtkinter.CTkLabel(self.Gest3Frame,text = f"Peace Sign", text_color = "white",font=("System", 23, "bold"))
        self.Gest3_LBl.grid(row=1, column=0, padx=20, pady=(20, 20))
        
        self.Shortcut3 = customtkinter.CTkEntry(self.Gest3Frame, width=100, placeholder_text="Enter Shortcut")
        self.Shortcut3.grid(row=2, column=0, padx=30, pady=(0, 15))
        
        self.Shortcut3_Btn = customtkinter.CTkButton(self.Gest3Frame,hover_color="orange", text="Set")
        self.Shortcut3_Btn.grid(row=3, column=0, padx=20, pady=(0, 20))
        
        #-----------------------------------------
        
        self.progressbar = customtkinter.CTkProgressBar(self.tabview.tab("View Patients"),width=800)
        self.progressbar.place(x=Main.winfo_screenwidth()/2 - 525,y=Main.winfo_screenheight()/2 - 90, anchor="center")

        self.progressbar.configure(mode="indeterminnate")
        self.progressbar.start()
        
        # self.Detect_Sign()
        
    def Detect_Sign(self):
        RMHand = mp.solutions.hands
        Hand = RMHand.Hands()

        cap = cv2.VideoCapture(1)

        screen_width, screen_height = pyautogui.size()

        x, y = 0, 0

        pinch_threshold = 25 

        while cap.isOpened():
            ret, Frame = cap.read()
            if not ret:
                continue

            self.Fist_Stat = self.Get_Fist_Stat.process_frame(Frame)
            print("Fist Stat: ",self.Fist_Stat)
            
            self.Pinch_Stat = self.Get_Pinch_Stat.process_frame(Frame)
            print(f"Pinch Status: {self.Pinch_Stat}")
            
            self.Peace_Stat = self.Get_Peace_Stat.process_frame(Frame)
            print(f"Peace Stat: {self.Peace_Stat}")
            
            frame_rgb = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGB)
            results = Hand.process(frame_rgb)
            
            
            if self.Fist_Stat == "Fist":
                pyautogui.hotkey('winleft', 'd')
            elif self.Pinch_Stat == "isPinch":
                pyautogui.click(button='left')
            elif self.Peace_Stat == "isPeace":
                pyautogui.hotkey('ctrl', 'winleft', 'o')

            canvas = np.zeros((Frame.shape[0], Frame.shape[1], 3), dtype=np.uint8)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    index_x = int(hand_landmarks.landmark[10].x * screen_width)
                    index_y = int(hand_landmarks.landmark[10].y * screen_height)

                    for landmark in hand_landmarks.landmark:
                        x_draw, y_draw = int(landmark.x * Frame.shape[1]), int(landmark.y * Frame.shape[0])
                        cv2.circle(Frame, (x_draw, y_draw), 5, (0, 0, 255), -1)

                    x, y = index_x, index_y

                    pyautogui.moveTo(x, y)

            result_frame = cv2.add(Frame, canvas)
            
            cv2.putText(result_frame, f"Status: {self.Fist_Stat}", (20, 30), cv2.FONT_HERSHEY_PLAIN, 1.2, (255, 0, 0), 2)

            cv2.imshow("Tracker", result_frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break
        
        cap.release()
        cv2.destroyAllWindows()

        pass

    def Set_Shortcuts(self):
        pass
      
    
    def Main_Screen(self):
        self.DestroyAll()

        Main.title("GestControl")
        Main.attributes("-topmost", True)

        self.ScreenWidth = Main.winfo_screenwidth()
        self.ScreenHeight = Main.winfo_screenheight()
        Main.geometry("700x580".format(self.ScreenWidth, self.ScreenHeight))

        self.WelcomeLabel = customtkinter.CTkLabel(Main, text="GestControl", font=("System", 40, "bold"))
        self.ContinueButton = customtkinter.CTkButton(Main, text="Continue", command=lambda: self.Continue(),  width=500, height=125, font=("System", 40, "bold"), fg_color="darkgreen")
        self.QuitButton = customtkinter.CTkButton(Main, text="Quit", command=quit, width=500, height=125, font=("System", 40, "bold"), fg_color="darkgreen")
        self.WelcomeLabel.place(x=self.ScreenWidth/2-610, y=self.ScreenHeight/2 - 450, anchor="center")
        self.ContinueButton.place(x=self.ScreenWidth/2 - 610, y=self.ScreenHeight/2 - 250, anchor="center")
        self.QuitButton.place(x=self.ScreenWidth/2 - 610, y=self.ScreenHeight/2 - 100, anchor="center")

gui = MainGUI()
def camera_thread():
    gui.Detect_Sign()

gui_thread = threading.Thread(target=gui.Main_Screen)
cam_thread = threading.Thread(target=camera_thread)

gui_thread.start()
cam_thread.start()


Main.mainloop()

