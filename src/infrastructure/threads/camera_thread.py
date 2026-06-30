from typing import Callable
import numpy as np
from PySide6.QtCore import QThread, QObject, Signal
import time

from src.domain.interfaces.i_camera_source import ICameraSource


class _Worker(QObject):
    
    frame_ready = Signal(object)
    head_pose_ready = Signal(object)
    brow_gesture_ready = Signal(object)
    blink_gesture_ready = Signal(object, object)

    def __init__(self, camera: ICameraSource, face_pipeline):
        super().__init__()
        self._camera  = camera
        self._face_pipeline = face_pipeline
        self._running = False

    def run(self) -> None:
        self._running = True
        try:
            self._camera.open()
            while self._running:
                frame = self._camera.get_frame()
                #ok, frame = self._camera.get_frame()
                #if not ok:
                #    break
                origin, cords, blink, brow_up = self._face_pipeline.process_frame(frame)
                self.frame_ready.emit(origin)
                self.head_pose_ready.emit(cords)
                self.blink_gesture_ready.emit(blink, cords)
                self.brow_gesture_ready.emit(brow_up)
        except Exception as e:
            pass
        finally:
            self._camera.close()

    def stop(self) -> None:
        self._running = False


class CameraThread:
    def __init__(self):
        self._thread: QThread | None  = None
        self._worker: _Worker | None  = None

    def start(self, 
              camera:   ICameraSource, 
              face_pipeline,
              on_frame: Callable[[np.ndarray], None],
              on_head_pose: Callable,
              on_brow_gesture: Callable,
              on_blink_gesture: Callable) -> None:
        
        if self.is_running():
            return

        self._thread = QThread()
        self._worker = _Worker(camera, face_pipeline)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)

        self._worker.frame_ready.connect(on_frame)
        self._worker.head_pose_ready.connect(on_head_pose)
        self._worker.brow_gesture_ready.connect(on_brow_gesture)
        self._worker.blink_gesture_ready.connect(on_blink_gesture)

        self._thread.start()

    def stop(self) -> None:
        if self._worker:
            self._worker.stop()
        if self._thread:
            self._thread.quit()
            self._thread.wait()

    def is_running(self) -> bool:
        return bool(self._thread and self._thread.isRunning())
