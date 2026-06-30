from PySide6.QtWidgets import QPushButton
class IntelliButton(QPushButton):
    def __init__(self, name = ''):
        super().__init__()
        self.setText(name)
        self.setMinimumHeight(140)
        self.setStyleSheet("""
            QPushButton {background-color: #16A085; color: white; font-size: 16px; border-radius: 6px;}
            QPushButton:hover { background-color: #1ABC9C; }
            QPushButton:pressed { background-color: #0E6655; }
            """)