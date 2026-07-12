from abc import ABC, abstractmethod

class IFaceGestureDetector(ABC):
    """
        Interface for the face gesture detection.
    """
    
    @abstractmethod
    def detectBlink(self) -> bool:
        """
        Detect if the eyes are closed based on the landmarks.
        
        returns:
            True if the eyes are closed, False otherwise
        """
        ...

    @abstractmethod
    def detectBrowUp(self) -> bool:
        """
        Detect if the eyebrows are raised based on the landmarks.
        
        returns:
            True if the eyebrows are raised, False otherwise
        """
        ...