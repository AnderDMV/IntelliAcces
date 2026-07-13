from src.domain.interfaces.i_detector import IDetector
from abc import ABC, abstractmethod
import numpy as np

class IDetectorsBuilder(ABC):
    """
        Interface for blink calcs
    """
    detectors_list : list[IDetector] = None
    
    def setFrames():
        for d in IDetectorsBuilder.detectors_list:
            d.frame = IDetectorsBuilder.frame
            
        
    @abstractmethod
    def detect(self, frame: np.ndarray):
        """
        Processes the frame by implementing facial detection AI and saving the processed frame.
        """
        self.frame =  frame
        