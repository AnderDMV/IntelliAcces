import sys
import pyautogui
import ctypes
import win_magnification as mag
import keyboard

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QCursor

#Codigo de ejemplo no modificar
class TrackingView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.resize(1920,1080)

        self.circle_pos = self.rect().center()
        self.radius = 60
        self.show_circle = True 

         # --- Aquí aplicamos los flags de Windows ---
        hwnd = int(self.winId())
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 0x00080000
        WS_EX_TRANSPARENT = 0x00000020
        user32 = ctypes.windll.user32
        style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | WS_EX_TRANSPARENT)

        # Timer para actualizar la posición
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_circle)
        self.timer.start(16)  # ~60 FPS

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_flags)
        self.timer.start(100)  # cada 100ms revisa

        
        self.zoom_flag = {"zoom_in": False, "zoom_out": False}

        #Hotkeys
        keyboard.add_hotkey("z", lambda: self.zoom_flag.update({"zoom_in": True}))
        keyboard.add_hotkey("x", lambda: self.zoom_flag.update({"zoom_out": True}))

    def aos(self):
        mag.set_fullscreen_transform(2.0, (480,270))

    def update_circle(self):
        self.circle_pos = self.mapFromGlobal(QCursor.pos())
        self.update() 

    def paintEvent(self, event):
        if not self.show_circle:
            self.show_circle = not self.show_circle
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Color semitransparente para el círculo
        painter.setBrush(QColor(0, 150, 255, 180))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.circle_pos, self.radius, self.radius)
        #print(self.circle_pos)

    def check_flags(self):
        if self.zoom_flag["zoom_in"]:
            self.radius = 15
            mag.set_fullscreen_transform(4.0, (QCursor.pos().x() - 480,QCursor.pos().y() - 270))
            self.zoom_flag["zoom_in"] = False
        if self.zoom_flag["zoom_out"]:
            self.radius = 60
            mag.reset_fullscreen_transform()
            self.zoom_flag["zoom_out"] = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mag.initialize()
    window = TrackingView()
    window.show()

    sys.exit(app.exec())
