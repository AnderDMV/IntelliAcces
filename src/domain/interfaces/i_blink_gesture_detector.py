from abc import ABC, abstractmethod
import numpy as np

class IBlinkGestureDetector(ABC):
    """
        Interface for blink calcs
    """
    
    @abstractmethod
    def is_blink(self) -> bool:
        """
        Detect if the eyes are closed based on the landmarks using the processed frame.

        returns:
            bool: True if the eyes are closed, False otherwise
        """
        ...
        