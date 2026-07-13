from src.domain.interfaces.i_blink_gesture_detector import IBlinkGestureDetector
from src.domain.interfaces.i_detector import IDetector

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from collections import deque

import mediapipe as mp
import numpy as np
import math

import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision

class BlinkGestureDetector(IBlinkGestureDetector, IDetector):

    _LEFT_EYE = [33, 160, 158, 133, 153, 144]

    _RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    _EAR_THRESH = 0.165

    _CLOSED_FRAMES = 0

    _REQUIRED_FRAMES = 3

    _BASELINE = None

    _WINDOW = deque(maxlen=5)
    
    def __init__(self):
        super().__init__()
        self.frame_processed = None
        
        
        
    def detect(self, frame: np.ndarray, timestamp_ms):
        """
        Processes the frame by implementing facial detection AI and saving the processed frame.
        """    
        if not BlinkGestureDetector.initialized:
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
            BlinkGestureDetector.initialized = True
        
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data = frame_RGB)
        
        self.frame_processed = self.detector.detect_for_video(mp_image, timestamp_ms)
            
        
    def is_blink(self) -> bool:
        """
        Detect if the eyes are closed based on the landmarks.

        Args:
            landmarks: The face landmarks detected by the model
        returns:
            bool: True if the eyes are closed, False otherwise
        """
        if self.frame_processed.face_landmarks:
            landmarks = self.frame_processed.face_landmarks[0]
            
            left_ear = self._eye_aspect_ratio(landmarks, self._LEFT_EYE)
            right_ear = self._eye_aspect_ratio(landmarks, self._RIGHT_EYE)

            eyes_closed = (left_ear < self._EAR_THRESH or right_ear < self._EAR_THRESH)

            #Update the frames counter 
            if eyes_closed:
                self._CLOSED_FRAMES += 1
            else:
                self._CLOSED_FRAMES = 0

            eyes_closed_confirmed = (self._CLOSED_FRAMES >= self._REQUIRED_FRAMES)
            return eyes_closed_confirmed    
        else : return False
        
        
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
    
    
        
    
        