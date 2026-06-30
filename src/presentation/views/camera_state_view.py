from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel
from PySide6.QtGui import QIcon, QImage, QPixmap
from PySide6.QtCore import Qt, QSize, Signal

from src.presentation.widgets.ip_buttons import IntelliButton

class CameraStateView(QWidget):
    back_clicked = Signal()

    def __init__(self):
        super().__init__()
        #Layout config
        pMainLayout = QVBoxLayout()
        pMainLayout.setContentsMargins(30,30,30,30)
        pMainLayout.setSpacing(0)    

        #label image camera
        self.label = QLabel(self)

        #back button
        exit_apps_ibutton = IntelliButton()
        exit_apps_ibutton.setIcon(QIcon("assets/icons/back.png"))
        exit_apps_ibutton.setIconSize(QSize(50,50))

        
        pMainLayout.addWidget(self.label)
        pMainLayout.addWidget(exit_apps_ibutton)
        self.setLayout(pMainLayout)
        
        exit_apps_ibutton.clicked.connect(self.back_clicked)

        
    def update_frame(self, img, h, w, bytes_per_line):
        # Convert the frame to a QPixmap and display it in the view
        qimg = QImage(img, w, h, bytes_per_line, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qimg))
