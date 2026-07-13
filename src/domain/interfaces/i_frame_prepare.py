from abc import ABC, abstractmethod

class IFramePrepare(ABC):
    """
        Prepara el frame
    """
    
    @abstractmethod
    def process(self) -> bool:
        """
        Open the camera to initialize capturing frames.

        Raises:
            RuntimeError: if the camera cannot be opened.
        """
        ...
        