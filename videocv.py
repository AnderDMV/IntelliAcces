import sys
import cv2
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Webcam en PySide6")

        # Layout y label
        self.label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Captura de cámara
        self.cap = cv2.VideoCapture(0)

        # Timer para refrescar frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # ~33ms → 30fps

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convertir BGR → RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Crear QImage desde numpy
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # Mostrar en QLabel
            self.label.setPixmap(QPixmap.fromImage(qimg))

    def closeEvent(self, event):
        self.cap.release()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CameraWidget()
    win.show()
    sys.exit(app.exec())
