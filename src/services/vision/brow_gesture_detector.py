from src.domain.interfaces.i_brow_up_gesture_detector import IBrowUpGestureDetector
from src.domain.interfaces.i_detector import IDetector

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from collections import deque

import mediapipe as mp
import numpy as np
import math

import cv2
import time
import mediapipe as mp
from mediapipe.tasks.python import vision

class BrowGestureDetector(IBrowUpGestureDetector, IDetector):
    
    _LEFT_EYE = [33, 160, 158, 133, 153, 144]

    _RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    _BROW = [65, 66, 70, 105, 107, 336, 296]

    _BASELINE = None

    _WINDOW = deque(maxlen=5)
    
    def __init__(self):
        super().__init__()
        self.frame_processed = None
        
        
    #Override from IBrowUpGestureDetector
    def is_brow_up(self) -> bool:
        """
        Detect if the eyebrows are raised based on the landmarks.

        Args:
            landmarks: The face landmarks detected by the model
        returns:
            bool: True if the eyebrows are raised, False otherwise
        """
                
        if self.frame_processed.face_landmarks:
            # AVG Brow
            landmarks = self.frame_processed.face_landmarks[0]
            
            brow_y = np.mean([landmarks[i].y for i in self._BROW])
            
            # AVG eyes Y POINT 33 and 263
            eye_y = (landmarks[self._LEFT_EYE[0]].y + landmarks[self._RIGHT_EYE[3]].y) / 2
            diff = eye_y - brow_y  

            self._WINDOW.append(diff)
            diff_smoothed = sum(self._WINDOW) / len(self._WINDOW)
            if self._BASELINE is None and len(self._WINDOW) == self._WINDOW.maxlen:
                self._BASELINE = diff_smoothed


            nose_y = landmarks[1].y
            pitch_factor = 1.0 + abs(nose_y - eye_y) * 2.0

            eyebrow_up_confirmed = self._BASELINE is not None and diff_smoothed > self._BASELINE + 0.015 * pitch_factor
            return eyebrow_up_confirmed
        else : return False
      
    #Override from IDetector   
    def detect(self, frame: np.ndarray, timestamp_ms):
        """
        Processes the frame by implementing facial detection AI and saving the processed frame.
        """    
        if not BrowGestureDetector.initialized:
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
            BrowGestureDetector.initialized = True
            
            
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data = frame_RGB)
        self.frame_processed = self.detector.detect_for_video(mp_image, timestamp_ms)
    
    
    #Private methods
    def _distance(self, p1, p2):
        return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2 
        )
    
    def _eye_aspect_ratio(self, landmarks, eye_indices):

        p1 = landmarks[eye_indices[0]]
        p2 = landmarks[eye_indices[1]]
        p3 = landmarks[eye_indices[2]]
        p4 = landmarks[eye_indices[3]]
        p5 = landmarks[eye_indices[4]]
        p6 = landmarks[eye_indices[5]]

        vertical_1 = self._distance(p2, p6)
        vertical_2 = self._distance(p3, p5)
        horizontal = self._distance(p1, p4)
        
        if horizontal == 0:
            return 0

        ear = (vertical_1 + vertical_2) / (2.0 * horizontal)

        return ear
    
    
        