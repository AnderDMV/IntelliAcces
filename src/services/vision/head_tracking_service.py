from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from collections import deque
import mediapipe as mp

import numpy as np
import math

LANDMARKS = {
    "left": 234,
    "right": 454,
    "top": 10,
    "bottom": 152,
    "front": 1,
}

class HeadTrackingService():
    
    def __init__(self):
        BaseOptions = mp.tasks.BaseOptions
        FaceLandmarker = vision.FaceLandmarker
        FaceLandmarkerOptions = vision.FaceLandmarkerOptions
        VisionRunningMode = vision.RunningMode

        options = FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path="src/services/vision/face_landmarker.task"),
            running_mode=VisionRunningMode.VIDEO, 
            num_faces=1
        )
        self.MONITOR_WIDTH = 1920
        self.MONITOR_HEIGHT = 1080

        self.calibration_offset_yaw = 0
        self.calibration_offset_pitch = 0

        self.filter_length = 8

        self.ray_origins = deque(maxlen=self.filter_length)
        self.ray_directions = deque(maxlen=self.filter_length)
        self.ray_directions = deque(maxlen=8)

        self.landmarker = FaceLandmarker.create_from_options(options)


    def _landmark_to_np(self, landmark, w, h):
        return np.array([
            landmark.x * w,
            landmark.y * h,
            landmark.z * w
        ])
    
    def getCords(self, face_landmarks, h, w):
        key_points = {}

        for name, idx in LANDMARKS.items():
            pt = self._landmark_to_np(face_landmarks[idx], w, h)
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

    def start_calibration(self):
        print('calibrando')
        self.calibration_offset_yaw = 180 - self.raw_yaw_deg
        self.calibration_offset_pitch = 180 - self.raw_pitch_deg
        
        