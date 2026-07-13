from abc import ABC, abstractmethod
import numpy as np

class IDetector(ABC):
    """
        Interface for blink calcs
    """
    initialized = False
    
    @abstractmethod
    def detect(self, frame: np.ndarray):
        """
        Processes the frame by implementing facial detection AI and saving the processed frame.
        """
        self.frame_processed =  frame        