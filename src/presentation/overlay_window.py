import ctypes
from PySide6.QtWidgets import  QWidget, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QCursor
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtCore import QPoint
import time

class OverlayWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.resize(1920,1080)

        #Settings
        self.hwnd = int(self.winId())
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 0x00080000
        WS_EX_TRANSPARENT = 0x00000020
        self.user32 = ctypes.windll.user32
        style = self.user32.GetWindowLongW(self.hwnd, GWL_EXSTYLE)
        self.user32.SetWindowLongW(self.hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | WS_EX_TRANSPARENT)

        SWP_NOSIZE = 0x0001
        SWP_NOMOVE = 0x0002
        SWP_NOACTIVATE = 0x0010
        HWND_TOPMOST = -1

        self.user32.SetWindowPos(self.hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                            SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE)
    
        #Layout window
        WMainLayout = QVBoxLayout(self)
        WMainLayout.setContentsMargins(0,0,0,0)
        WMainLayout.setSpacing(0)    

        self.circle_pos = self.rect().center()
        self.radius = 60
        self.show_circle = True 

        
    def move_circle(self, cords):
        if cords is None:
            self.circle_pos = QPoint(500,500)
            SWP_NOSIZE = 0x0001
            SWP_NOMOVE = 0x0002
            SWP_NOACTIVATE = 0x0010
            HWND_TOPMOST = -1
            self.user32.SetWindowPos(self.hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                                 SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE)
            self.update()
        else:
            self.circle_pos = QPoint(cords[0], cords[1])
            self.update()

    def update_circle(self):
        self.circle_pos = self.mapFromGlobal(QCursor.pos())
        self.update() 

    def paintEvent(self, event):
        if not self.show_circle:
            self.show_circle = not self.show_circle
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(0, 150, 255, 180))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.circle_pos, self.radius, self.radius)
        #print(self.circle_pos)

    """def check_flags(self):
        if self.zoom_flag["zoom_in"]:
            mag.set_fullscreen_transform(2.0, (QCursor.pos().x() - 480,QCursor.pos().y() - 270))
            self.zoom_flag["zoom_in"] = False
        if self.zoom_flag["zoom_out"]:
            mag.reset_fullscreen_transform()
            self.zoom_flag["zoom_out"] = False"""

        
