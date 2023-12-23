import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import math
from mediapipe.framework.formats import landmark_pb2
import matplotlib.pyplot as plt
import os
import time

class Fist_Recognizer:
    # def __init__(self):
    #     self.mp_hands = mp.solutions.hands
    #     self.hands = self.mp_hands.Hands()
    #     self.request_status = "idle"

    # def is_fist(self, hand_landmarks):
    #     thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
    #     pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]

    #     thumb_y = thumb_tip.y
    #     pinky_y = pinky_tip.y

    #     if abs(thumb_y - pinky_y) < 0.1:
    #         return True
    #     else:
    #         return False

    # def process_frame(self, frame):
    #     frame = cv2.flip(frame, 1)
    #     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     results = self.hands.process(frame_rgb)

    #     if results.multi_hand_landmarks:
    #         for hand_landmarks in results.multi_hand_landmarks:
    #             # Check for the fist gesture
    #             if self.is_fist(hand_landmarks):
    #                 self.request_status = "Fist"
    #             else:
    #                 self.request_status = "Deactivate"

    #     return self.request_status
    def __init__(self):
        plt.rcParams.update({
            'axes.spines.top': False,
            'axes.spines.right': False,
            'axes.spines.left': False,
            'axes.spines.bottom': False,
            'xtick.labelbottom': False,
            'xtick.bottom': False,
            'ytick.labelleft': False,
            'ytick.left': False,
            'xtick.labeltop': False,
            'xtick.top': False,
            'ytick.labelright': False,
            'ytick.right': False
        })
        
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.path = self.script_directory + 'Model/Fist_Recog.task'
        self.base_options = python.BaseOptions(model_asset_path=self.path)
        options = vision.GestureRecognizerOptions(base_options=self.base_options)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)
        self.request_status = "idle"

    def process_frame(self, frame):

        frame = cv2.flip(frame, 1)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        recognition_result = self.recognizer.recognize(image)

        if recognition_result.gestures:
            top_gesture = recognition_result.gestures[0][0]
            print(top_gesture)

            # hand_landmarks = recognition_result.hand_landmarks
            results = top_gesture

            if results.category_name == "Open_Palm":
                self.request_status = "Deactivated"
            elif results.category_name == "Closed_Fist":
                self.request_status = "Fist"

        # cv2.imshow('Hand Tracking', frame)
        return self.request_status
    
class Pinch_Recognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.request_status = "idle"
        self.pinch_start_time = None

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

                thumb_x, thumb_y = int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])
                index_x, index_y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])

                distance = ((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2) ** 0.5

                pinch_threshold = 30 

                if distance < pinch_threshold:
                    if self.request_status != "isPinch":
                        self.pinch_start_time = time.time()  
                    self.request_status = "isPinch"
                else:
                    self.request_status = "Deactivated"
                    self.pinch_start_time = None  


        if self.request_status == "isPinch" and self.pinch_start_time is not None:
            current_time = time.time()
            pinch_duration = current_time - self.pinch_start_time
            if pinch_duration > 1.0:
                self.request_status = "hold"

        return self.request_status
    
class Peace_Detector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.request_status = "idle"

    def is_peace_sign(self, hand_landmarks):
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

        index_y = index_tip.y
        middle_y = middle_tip.y

        if index_y < middle_y:
            return True
        else:
            return False

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if self.is_peace_sign(hand_landmarks):
                    self.request_status = "isPeace"
                else:
                    self.request_status = "Deactivate"

        return self.request_status
