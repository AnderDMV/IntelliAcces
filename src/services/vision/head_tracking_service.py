from src.domain.interfaces.i_head_tracking_service import IHeadTrackingService
from src.domain.interfaces.i_detector import IDetector

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from collections import deque
import mediapipe as mp

import cv2

import numpy as np
import math


LANDMARKS = {
    "left": 234,
    "right": 454,
    "top": 10,
    "bottom": 152,
    "front": 1,
}

class HeadTrackingService(IHeadTrackingService, IDetector):
    """
    Performs head tracking using facial recognition with facial landmarks.
    
    Implementation of the IHeadTrackingService interface using MediaPipe for head tracking, using facial landmarks to determine the position and orientation of the head in relation to the screen.
    Use getCords to get the coordinates of the head based on the face landmarks, and start_calibration to calibrate the head tracking system.

    attributes:
        MONITOR_WIDTH (int): The width of the monitor in pixels.
        MONITOR_HEIGHT (int): The height of the monitor in pixels.
        calibration_offset_yaw (float): The yaw offset for calibration.
        calibration_offset_pitch (float): The pitch offset for calibration.
        filter_length (int): The length of the filter for smoothing the head tracking data.
        ray_origins (deque): A deque to store the origins of the rays for smoothing.
        ray_directions (deque): A deque to store the directions of the rays for smoothing.
    """
    
    def __init__(self):
        self.MONITOR_WIDTH = 1920
        self.MONITOR_HEIGHT = 1080

        self.calibration_offset_yaw = 0
        self.calibration_offset_pitch = 0

        self.filter_length = 8

        self.ray_origins = deque(maxlen=self.filter_length)
        self.ray_directions = deque(maxlen=self.filter_length)
        self.ray_directions = deque(maxlen=8)

        self.frame_processed = None


    def _landmark_to_np(self, landmark, w, h):
        """Convert a MediaPipe landmark to a numpy array with pixel coordinates."""
        return np.array([
            landmark.x * w,
            landmark.y * h,
            landmark.z * w
        ])
    
    def detect(self, frame: np.ndarray, timestamp_ms):
        """
        Processes the frame by implementing facial detection AI and saving the processed frame.
        """
        if not HeadTrackingService.initialized:
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
            HeadTrackingService.initialized = True
                
        self.frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data = self.frame_RGB)
        
        self.h = self.frame_RGB.shape[0] 
        self.w = self.frame_RGB.shape[1]
        self.frame_processed = self.detector.detect_for_video(mp_image, timestamp_ms)
        
    
    def getCords(self):
        if self.frame_processed.face_landmarks: 
            key_points = {}

            landmarks = self.frame_processed.face_landmarks[0]
            
            for name, idx in LANDMARKS.items():
                pt = self._landmark_to_np(landmarks[idx], self.w, self.h)
                key_points[name] = pt


            # Extract points
            left = key_points["left"]
            right = key_points["right"]
            top = key_points["top"]
            bottom = key_points["bottom"]
            front = key_points["front"]

            # Oriented axes based on head geometry
            right_axis = (right - left)
            right_axis /= np.linalg.norm(right_axis)

            up_axis = (top - bottom)
            up_axis /= np.linalg.norm(up_axis)

            forward_axis = np.cross(right_axis, up_axis)
            forward_axis /= np.linalg.norm(forward_axis)

            # Flip to ensure forward vector comes out of the face
            forward_axis = -forward_axis

            # Compute center of the head
            center = (left + right + top + bottom + front) / 5

            # Half-sizes (width, height, depth)
            half_width = np.linalg.norm(right - left) / 2
            half_height = np.linalg.norm(top - bottom) / 2
            half_depth = 80  # can be tuned or calculated if you have a back landmark

            # Update smoothing buffers
            self.ray_origins.append(center)
            self.ray_directions.append(forward_axis)

            # Compute averaged ray origin and direction
            avg_origin = np.mean(self.ray_origins, axis=0)
            avg_direction = np.mean(self.ray_directions, axis=0)
            avg_direction /= np.linalg.norm(avg_direction)  # normalize

            # Reference forward direction (camera looking straight ahead)
            reference_forward = np.array([0, 0, -1])  # Z-axis into the screen

            # Horizontal (yaw) angle from reference (project onto XZ plane)
            xz_proj = np.array([avg_direction[0], 0, avg_direction[2]])
            xz_proj /= np.linalg.norm(xz_proj)
            yaw_rad = math.acos(np.clip(np.dot(reference_forward, xz_proj), -1.0, 1.0))
            if avg_direction[0] < 0:
                yaw_rad = -yaw_rad  # left is negative

            # Vertical (pitch) angle from reference (project onto YZ plane)
            yz_proj = np.array([0, avg_direction[1], avg_direction[2]])
            yz_proj /= np.linalg.norm(yz_proj)
            pitch_rad = math.acos(np.clip(np.dot(reference_forward, yz_proj), -1.0, 1.0))
            if avg_direction[1] > 0:
                pitch_rad = -pitch_rad  # up is positive

            #Specify 

            # Convert to degrees and re-center around 0
            yaw_deg = np.degrees(yaw_rad)
            pitch_deg = np.degrees(pitch_rad)

            #this results in the center being 180, +10 left = -170, +10 right = +170

            #convert left rotations to 0-180
            if yaw_deg < 0:
                yaw_deg = abs(yaw_deg)
            elif yaw_deg < 180:
                yaw_deg = 360 - yaw_deg

            if pitch_deg < 0:
                pitch_deg = 360 + pitch_deg

            self.raw_yaw_deg = yaw_deg
            self.raw_pitch_deg = pitch_deg
            
            #yaw is now converted to 90 (looking directly left) to 270 (looking directly right), wrt camera
            #pitch is now converted to 90 (looking straight down) and 270 (looking straight up), wrt camera
            #print(f"Angles: yaw={yaw_deg}, pitch={pitch_deg}")

            #specify degrees at which screen border will be reached
            yawDegrees = 20 # x degrees left or right
            pitchDegrees = 10 # x degrees up or down
            
            # leftmost pixel position must correspond to 180 - yaw degrees
            # rightmost pixel position must correspond to 180 + yaw degrees
            # topmost pixel position must correspond to 180 + pitch degrees
            # bottommost pixel position must correspond to 180 - pitch degrees

            # Apply calibration offsets
            yaw_deg += self.calibration_offset_yaw
            pitch_deg += self.calibration_offset_pitch

            # Map to full screen resolution
            screen_x = int(((yaw_deg - (180 - yawDegrees)) / (2 * yawDegrees)) * self.MONITOR_WIDTH)
            screen_y = int(((180 + pitchDegrees - pitch_deg) / (2 * pitchDegrees)) * self.MONITOR_HEIGHT)

            # Clamp screen position to monitor bounds
            if(screen_x < 10):
                screen_x = 10
            if(screen_y < 10):
                screen_y = 10
            if(screen_x > self.MONITOR_WIDTH - 10):
                screen_x = self.MONITOR_WIDTH - 10
            if(screen_y > self.MONITOR_HEIGHT - 10):
                screen_y = self.MONITOR_HEIGHT - 10
            #########################################################################
            return (screen_x, screen_y)
        else : return None

    def get_frames(self):
        self.frame_RGB_landmarks = self.frame_RGB.copy()
        if self.frame_processed.face_landmarks:
            for landmark in self.frame_processed.face_landmarks[0]:
                x = int(landmark.x * self.w)
                y = int(landmark.y * self.h)
                self.frame_RGB_landmarks[y, x] = (255,255,255)
        return (self.frame_RGB, self.frame_RGB_landmarks)
    
    
    def start_calibration(self):
        print('calibrando')
        self.calibration_offset_yaw = 180 - self.raw_yaw_deg
        self.calibration_offset_pitch = 180 - self.raw_pitch_deg
        
