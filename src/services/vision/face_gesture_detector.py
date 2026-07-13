from src.domain.interfaces.i_detector import IDetector
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from collections import deque

import mediapipe as mp
import cv2
import numpy as np
import math

class FaceGestureDetector():

    detectors_list : list[IDetector] = None
    def __init__(self):
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
        
    def build(self, frame, timestamp_ms):
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data = frame_RGB)
        self.frame_processed = self.detector.detect_for_video(mp_image, timestamp_ms)
        
        for det in self.detectors_list:
            det.initialized = True
            det.frame_processed = self.frame_processed
        