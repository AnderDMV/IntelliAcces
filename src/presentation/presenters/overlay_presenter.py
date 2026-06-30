import numpy as np
from src.services.actions.mouse_controller import MouseController
import time
import pyautogui

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
        
        self.last_blink = int(time.time() * 1000)
        self.last_brow_gesture = int(time.time() * 1000)

        self._clickedState = False
        self._blink_ready = False
        self._brow_gesture_ready = False

    def _on_frame(self, frame):
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        if self._state_view.isVisible():
            self._state_view.update_frame(frame.data, h, w, bytes_per_line)
        if self._calibration_view.isVisible():
            self._calibration_view.update_frame(frame.data, h, w, bytes_per_line)
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
        #Check the difference between `last_blink` and `now_blink`; if it exceeds 1500, stop the calculation and set `blink_ready` to `True`.
        if not self._blink_ready:
            now_blink = int(time.time() * 1000)
            rest = (self.last_blink - now_blink) * -1
            if rest >= 1500 :  self._blink_ready = True
        
        if blink and self._clickedState and self._blink_ready:
            self.last_blink = now_blink
            x,y = cords
            #pyautogui.click(x, y) 
            mc =  MouseController()
            mc.click_at(x, y)
            mc.move_to(1,1, duration=0)
            #pyautogui.moveTo(x, y, duration=0.2)
        if self._calibration_view.isVisible() and blink:
            
            self._face_pipeline.head_tracker.start_calibration()
# Hace clic en esa posición
        else:
            pass

    def _on_brow_gesture(self, brow: bool):
        #Check the difference between `last_brow` and `now_brow`; if it exceeds 1500, stop the calculation and set `brow_gesture_ready` to `True`.
        if not self._brow_gesture_ready:
            now_brow_gesture = int(time.time() * 1000)
            rest = (self.last_brow_gesture - now_brow_gesture) * -1
            if rest >= 2000 :  self._brow_gesture_ready = True
        

        if brow and self._brow_gesture_ready:
            self.last_brow_gesture = now_brow_gesture
            print('detect brow up', self._clickedState)
            if not self.used:
                self._clickedState = not self._clickedState
                self.used = True
        else:
            self.used = False
            pass