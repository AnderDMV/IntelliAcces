from abc import ABC, abstractmethod
import numpy as np

class IBrowUpGestureDetector(ABC):
    """
        Interface for blink calcs
    """
    
    @abstractmethod
    def is_brow_up(self) -> bool:
        """
        Detect if the eyes are closed based on the landmarks using the processed frame.

        returns:
            bool: True if the eyes are closed, False otherwise
        """
        ...
        