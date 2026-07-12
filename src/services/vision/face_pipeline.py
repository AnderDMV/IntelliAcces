from src.services.vision.face_gesture_detector import FaceGestureDetector
from src.services.vision.head_tracking_service import HeadTrackingService

from src.domain.interfaces.i_face_gesture_detector import IFaceGestureDetector
from src.domain.interfaces.i_head_tracking_service import IHeadTrackingService

import cv2
import time
import mediapipe as mp
from mediapipe.tasks.python import vision


import numpy as np

class FacePipeline():
    """Pipeline for facial processing using MediaPipe.

    This pipeline receives video frames, detects facial landmarks,
    computes head coordinates, and identifies facial gestures such
    as blinking and brow raising. It integrates head tracking and
    gesture detection services.
    """
    def __init__(self, head_tracker: IHeadTrackingService, gesture_detector: IFaceGestureDetector):
        """Initializes the FacePipeline with head tracking and gesture detection services.

        Args:
            head_tracker (HeadTrackingService): Service for computing head coordinates.
            gesture_detector (FaceGestureDetector): Service for detecting facial gestures.
        """
        
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
        """Processes a single frame to detect facial landmarks and gestures.

        Steps:
            1. Convert frame to RGB.
            2. Detect facial landmarks using MediaPipe.
            3. Compute head coordinates.
            4. Detect gestures (blink, brow up).
            5. Mark landmarks on a copy of the frame.

        Args:
            frame (np.ndarray): Input frame in BGR format.

        Returns:
            tuple: A tuple containing:
                - frame_RGB (np.ndarray): Original frame converted to RGB.
                - frame_RGB_landmarks (np.ndarray): Frame with landmarks marked.
                - cords (tuple | None): Head coordinates if detected, else None.
                - blink (bool): True if blink detected, False otherwise.
                - brow_up (bool): True if brow raise detected, False otherwise.
        """
        
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_RGB_landmarks = frame_RGB.copy()
        timestamp_ms = int(time.time() * 1000)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_RGB)
        result = self.detector.detect_for_video(mp_image, timestamp_ms)

        if result.face_landmarks:
            landmarks = result.face_landmarks[0]
            cords = self.head_tracker.getCords(landmarks, frame_RGB.shape[0], frame_RGB.shape[1])
            blink = self.gesture_detector.detectBlink(landmarks)
            brow_up = self.gesture_detector.detectBrowUp(landmarks)
            self._mark_points_frame(frame_RGB_landmarks, landmarks, frame_RGB.shape[1], frame_RGB.shape[0])
            return(frame_RGB, frame_RGB_landmarks, cords, blink, brow_up)
        else:
            return(frame_RGB, frame_RGB, None, False, False)
        
    def _mark_points_frame(self, frame,landmarks, w, h):
        for landmark in landmarks:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            frame[y, x] = (255,255,255)