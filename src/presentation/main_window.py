from PySide6.QtWidgets import  QWidget, QVBoxLayout, QStackedWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        #Settings window
        self.setWindowTitle("Intelli Acces")
        self.resize(800, 800)
        self.setMinimumSize(800, 800) 
        self.setMaximumSize(800, 800)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: #101831;")
        
        #Layout window
        WMainLayout = QVBoxLayout(self)
        WMainLayout.setContentsMargins(0,0,0,0)
        WMainLayout.setSpacing(0)    

        #Stack contains the views
        self.stack = QStackedWidget()
        
        WMainLayout.addWidget(self.stack)
        self.setLayout(WMainLayout)
    
    def add_view(self, view):
        self.stack.addWidget(view)

    def show_view(self, view, w, h):
        self.stack.setCurrentWidget(view)

        self.resize(w, h)
        self.setMinimumSize(w, h)  
        self.setMaximumSize(w, h)

        #centering of the view
        monitor = QGuiApplication.primaryScreen().geometry()
        x = (monitor.width() - w) // 2
        y = (monitor.height() - h) // 2
        self.move(x, y)
