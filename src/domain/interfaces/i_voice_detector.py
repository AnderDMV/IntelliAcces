from abc import ABC, abstractmethod

class IVoiceDetector(ABC):
    """
        Interface for blink calcs
    """
    
    @abstractmethod
    def process(self):
        """
        Detect if the eyes are closed based on the landmarks using the processed frame.

        returns:
            bool: True if the eyes are closed, False otherwise
        """
        ...
        
    def finish(self):
        ...