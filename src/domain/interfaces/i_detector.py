from abc import ABC, abstractmethod
import numpy as np

class IDetector(ABC):
    """
        Interface for detectors class type
    attributes:
    initialized (bool) bool to initialize general configuration once
    """
    initialized = False
    
    @abstractmethod
    def detect(self, frame: np.ndarray):
        """
        Processes the frame by implementing facial detection AI and configuration, saving the processed frame with the detections (face landmarks or others).
        """
        self.frame_processed =  frame        