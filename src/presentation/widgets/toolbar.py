from PySide6.QtWidgets import QFrame,QHBoxLayout, QLabel
from PySide6.QtCore import Qt


class ToolBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #192F52;")
        self.setMinimumHeight(50)
        self.setMaximumHeight(50)

        tittle = QLabel("Titulo")
        tittle.setAlignment(Qt.AlignCenter) 
        tittle.setStyleSheet("""
        QLabel {
        color: white;               /* Color del texto */
        font-size: 20px;          /* Tamaño */
        font-weight: bold;        /* Negrita */
        }
        """)

        TPanelLayout = QHBoxLayout()
        TPanelLayout.addWidget(tittle)
        self.setLayout(TPanelLayout)