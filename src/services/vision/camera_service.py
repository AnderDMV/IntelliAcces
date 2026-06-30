import cv2
import time

class CameraService:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        #timestamp_ms = int(time.time() * 1000)
        #return (cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), timestamp_ms)
        return frame

    def release(self):
        self.cap.release()

    def open(self) -> None:
        self._cap = cv2.VideoCapture(0)
        if not self._cap.isOpened():
            raise RuntimeError(f"No se pudo abrir la cámara {self._index}")

    def close(self) -> None:
        #if self._cap:
        #    self._cap.release()
        #    self._cap = None
        pass