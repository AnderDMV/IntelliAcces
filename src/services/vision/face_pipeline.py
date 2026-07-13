from src.domain.interfaces.i_blink_gesture_detector import IBlinkGestureDetector
from src.domain.interfaces.i_brow_up_gesture_detector import IBrowUpGestureDetector 
from src.domain.interfaces.i_head_tracking_service import IHeadTrackingService

import time
import numpy as np

class FacePipeline():
    """Pipeline for facial processing using MediaPipe.

    This pipeline receives video frames, detects facial landmarks,
    computes head coordinates, and identifies facial gestures such
    as blinking and brow raising. It integrates head tracking and
    gesture detection services.
    """
    def __init__(self, head_tracker: IHeadTrackingService, blink_gesture_detector: IBlinkGestureDetector, brow_gesture_detector: IBrowUpGestureDetector):
        """Initializes the FacePipeline with head tracking and gesture detection services.

        Args:
            head_tracker (HeadTrackingService): Service for computing head coordinates.
            gesture_detector (FaceGestureDetector): Service for detecting facial gestures.
        """
        self.head_tracker = head_tracker
        self.blink_gesture_detector = blink_gesture_detector
        self.brow_gesture_detector = brow_gesture_detector


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
        timestamp_ms = int(time.time() * 1000)
        
        self.head_tracker.detect(frame, timestamp_ms)
        self.blink_gesture_detector.detect(frame, timestamp_ms)
        self.brow_gesture_detector.detect(frame, timestamp_ms)
            
        cords = self.head_tracker.getCords()
        blink = self.blink_gesture_detector.is_blink()        
        brow_up = self.brow_gesture_detector.is_brow_up()
        frame_RGB, frame_RGB_landmarks = self.head_tracker.get_frames()
        
        return(frame_RGB, frame_RGB_landmarks, cords, blink, brow_up)
        