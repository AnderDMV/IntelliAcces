import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFrame
from PySide6.QtCore import Qt


class WindowMain(QWidget):
    def __init__(self):
        super().__init__()
        #Settings window
        self.setWindowTitle("Ejemplo PySide6")
        self.resize(500, 300)
        self.move(200, 100)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        frame = QFrame(self)
        frame.setStyleSheet("background-color: lightgreen;")

        layout = QVBoxLayout(frame)
        layout.addWidget(QPushButton("Botón 1"))
        layout.addWidget(QPushButton("Botón 2"))

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(frame)
        self.setLayout(main_layout)


    def mensaje(self):
        print('ada')    
