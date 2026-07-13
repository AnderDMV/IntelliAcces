from abc import ABC, abstractmethod
import numpy as np

class IHeadTrackingService(ABC):
    """
        Interface for the head tracking service
    """
    
    @abstractmethod
    def getCords(self, face_landmarks, h, w):
        """Get the coordinates of the head based on the face landmarks.
        
        Args:
            face_landmarks: The face landmarks detected by the model
            h: The height of the image
            w: The width of the image
        returns:
            A dictionary containing the coordinates of the head in relation to the screen (x,y)
        """
        ...

    @abstractmethod
    def start_calibration(self):
        """Start the calibration process"""
        ...
    
        
    @abstractmethod
    def get_frames():
        """
        Processes the frame by implementing facial detection AI and saving the processed frame.
        """
        ...