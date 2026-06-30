from src.services.vision.face_gesture_detector import FaceGestureDetector
from src.services.vision.head_tracking_service import HeadTrackingService

import cv2
import time
import mediapipe as mp
from mediapipe.tasks.python import vision


import numpy as np

class FacePipeline():

    def __init__(self, head_tracker: HeadTrackingService, gesture_detector: FaceGestureDetector):
        self.head_tracker = head_tracker
        self.gesture_detector = gesture_detector

        base_options = mp.tasks.BaseOptions
        face_landmarker = vision.FaceLandmarker
        face_landmarker_options = vision.FaceLandmarkerOptions
        vision_running_mode = vision.RunningMode

        options = face_landmarker_options(
            base_options = base_options(model_asset_path="src/services/vision/face_landmarker.task"),
            running_mode = vision_running_mode.VIDEO, 
            num_faces=1
        )

        self.detector = face_landmarker.create_from_options(options)

    def process_frame(self, frame: np.ndarray):
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        timestamp_ms = int(time.time() * 1000)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_RGB)
        result = self.detector.detect_for_video(mp_image, timestamp_ms)

        if result.face_landmarks:
            landmarks = result.face_landmarks[0]
            cords = self.head_tracker.getCords(landmarks, frame_RGB.shape[0], frame_RGB.shape[1])
            blink = self.gesture_detector.detectBlink(landmarks)
            brow_up = self.gesture_detector.detectBrowUp(landmarks)
            return(frame_RGB, cords, blink, brow_up)
        else:
            return(frame_RGB, None, False, False)
        
    def mark_points_frame(self, landmarks):
        pass