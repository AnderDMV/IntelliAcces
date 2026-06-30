from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, Signal

from src.presentation.widgets.ip_buttons import IntelliButton

class AppsSelectorView(QWidget):
    exit_clicked = Signal()

    def __init__(self):
        super().__init__()
        #Layout config
        pMainLayout = QVBoxLayout()
        pMainLayout.setContentsMargins(30,30,30,30)
        pMainLayout.setSpacing(0)    

        #exit button
        exit_apps_select_ibutton = IntelliButton()
        exit_apps_select_ibutton.setIcon(QIcon("assets/icons/back.png"))
        exit_apps_select_ibutton.setIconSize(QSize(50,50))

        pMainLayout.addWidget(exit_apps_select_ibutton)
        self.setLayout(pMainLayout)

        #Connections for buttons
        exit_apps_select_ibutton.clicked.connect(self.exit_clicked)

