from abc import ABC, abstractmethod

class ICameraSource(ABC):
    """
        Interface for the camera service
    """
    
    @abstractmethod
    def open(self):
        """
        Open the camera to initialize capturing frames.

        Raises:
            RuntimeError: if the camera cannot be opened.
        """
        ...

    @abstractmethod
    def close(self):
        """
        Close the camera and release the resource.
        """
        ...

    @abstractmethod
    def get_frame(self):
        """
        Capture a frame from the camera and return the image data.
        """
        ...