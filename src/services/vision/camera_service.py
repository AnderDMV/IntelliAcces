from src.domain.interfaces.i_camera_source import ICameraSource
import cv2

class CameraService(ICameraSource):
    """
    Service for handling camera operations.
    
    This service provides methods to open the camera, capture frames, and release the camera resource.
    It uses OpenCV's VideoCapture for camera access.
    """

    def __init__(self, camera_index = 0):
        """
        Initialize the CameraService with the specified camera index.

        Args:
            camera_index (int): Index of the camera (0 for the default camera).
        """
        self._index = camera_index
        self._cap: cv2.VideoCapture | None = None

    def open(self) -> None:
        if self._cap and self._cap.isOpened():
            return
            
        self._cap = cv2.VideoCapture(self._index)
        if not self._cap.isOpened():
            raise RuntimeError(f"No se pudo abrir la cámara con índice {self._index}")
        

    def get_frame(self):
        """
        Capture a frame from the camera and return it as a numpy array in RGB format
        
        Returns:
            np.ndarray | None: The captured frame in RGB format or None if unsuccessful.
        """
        ret, frame = self._cap.read()
        if not ret : return None
        return frame

    def _release(self):
        """Release the camera resource when done capturing frames."""
        self._cap.release()

    def close(self) -> None:
        if self._cap:
            self._cap.release()
            self._cap = None