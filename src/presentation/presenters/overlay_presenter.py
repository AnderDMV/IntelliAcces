import numpy as np
from src.services.actions.mouse_controller import MouseController
import time

BLINK_COOLDOWN_MS = 1500
BROW_COOLDOWN_MS = 2000

class OverlayPresenter():
    def __init__(self, view, calibration_view, state_view,  camera_thread, camera_service, face_pipeline):
        self._view = view
        self._calibration_view = calibration_view
        self._state_view = state_view
        #self._head_tracking_service = head_tracking_service
        self._face_pipeline = face_pipeline
        self._camera_thread = camera_thread
        self._camera_service = camera_service

        self._camera_thread.start(self._camera_service,
                                  self._face_pipeline, 
                                  self._on_frame,
                                  self._on_head_pose,
                                  self._on_brow_gesture,
                                  self._on_blink_gesture)
        
        self.last_blink = int(time.monotonic() * 1000)
        self.last_brow_gesture = int(time.monotonic() * 1000)

        self._clickedState = False
        self._blink_ready = False
        self._brow_gesture_ready = False

        self._brow_in_progress = False
        self._blink_in_progress = False

    def _on_frame(self, frame):
        h, w, ch = frame[0].shape
        bytes_per_line = ch * w
        if self._state_view.isVisible():
            self._state_view.update_frame(frame[0].data, h, w, bytes_per_line)
        if self._calibration_view.isVisible():
            self._calibration_view.update_frame(frame[1].data, h, w, bytes_per_line)
        #self._view.overlay_window_circle_move.emit(self._head_tracking_service.getCords(frame, timestamp))
        #self._view.move_circle(self._head_tracking_service.getCords(frame, timestamp))

    def _on_head_pose(self, cords: tuple):
        self._view.move_circle(cords)
        if self._calibration_view.isVisible():
            if cords is not None:
                self._calibration_view.update_face_state(True)
            else:
                self._calibration_view.update_face_state(False)

    def _on_blink_gesture(self, blink: bool, cords):
        #Check the difference between `last_blink` and `now_blink`; if it exceeds BLINK_COOLDOWN_MS, stop the calculation and set `blink_ready` to `True`.
        if not self._blink_ready:
            self.now_blink = int(time.monotonic() * 1000)
            rest = (self.last_blink - self.now_blink) * -1
            if rest >= BLINK_COOLDOWN_MS:  
                self._blink_ready = True
        
        if blink and self._clickedState and self._blink_ready and not self._blink_in_progress:
            self._blink_in_progress = True
            self.last_blink = self.now_blink
            self._blink_ready = False
            x,y = cords
            mc =  MouseController()
            mc.click_at(x, y)
            mc.move_to(2,2, duration=0)

        if self._calibration_view.isVisible() and blink and self._blink_ready and not self._blink_in_progress:
            self._blink_in_progress = True
            self.last_blink = self.now_blink
            self._blink_ready = False
            self._face_pipeline.head_tracker.start_calibration()
        if not blink and self._blink_in_progress:
            self._blink_in_progress = False

    def _on_brow_gesture(self, brow: bool):
        #Check the difference between `last_brow` and `now_brow`; if it exceeds BROW_COOLDOWN_MS, stop the calculation and set `brow_gesture_ready` to `True`.
        if not self._brow_gesture_ready:
            self.now_brow_gesture = int(time.monotonic() * 1000)
            rest = (self.last_brow_gesture - self.now_brow_gesture) * -1
            if rest >= BROW_COOLDOWN_MS:  
                self._brow_gesture_ready = True
        
        if brow and self._brow_gesture_ready and not self._brow_in_progress:
            self._brow_in_progress = True
            self.last_brow_gesture = self.now_brow_gesture
            self._brow_gesture_ready = False
            self._view.set_active_state(not self._view.is_active)
            self._clickedState = not self._clickedState
            print('detect brow up', self._clickedState)
        
        if not brow and self._brow_in_progress:
            print('cambio')
            self._brow_in_progress = False
