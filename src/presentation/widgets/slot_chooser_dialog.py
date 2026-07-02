# src/presentation/views/widgets/slot_chooser_dialog.py

import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QGridLayout, QPushButton
from PySide6.QtGui import QColor, QPainter, QPen, QLinearGradient, QPainterPath, QPixmap
from PySide6.QtCore import Qt, QRectF

class SlotChooserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Apariencia general
        self.setWindowTitle("Intelli Acces")
        self.resize(520, 520)
        self.setMinimumSize(520, 520)
        self.setMaximumSize(520, 520)
        self.setStyleSheet("background-color: #406EA8;")

        self.chosen_slot = None

        # Layout principal (¡importante pasar self!)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(18)

        # Título
        title = QLabel("Selecciona la posición donde guardar la aplicación")
        title.setStyleSheet("color: #5CE1FF; font-size: 22px; font-weight: bold; background: transparent;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Rejilla de slots
        grid = QGridLayout()
        grid.setSpacing(18)

        index = 0
        for row in range(3):
            for col in range(3):
                card = SlotCard(str(index), "assets/icons/signo-de-mas.png")
                card.clicked.connect(lambda _, i=index: self._choose_slot(i))
                grid.addWidget(card, row, col)
                index += 1

        layout.addLayout(grid)

    def _choose_slot(self, index: int):
        self.chosen_slot = index
        self.accept()


class SlotCard(QPushButton):
    def __init__(self, title, icon_path):
        super().__init__()
        self.title = title
        self.icon_path = icon_path
        self.setFixedSize(130, 130)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("background: transparent; border: none;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(4, 4, self.width()-8, self.height()-8)
        path = QPainterPath()
        path.addRoundedRect(rect, 20, 20)

        # Fondo con gradiente
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(26, 44, 70, 235))
        gradient.setColorAt(1.0, QColor(13, 21, 43, 245))
        painter.fillPath(path, gradient)

        # Borde
        border_color = QColor("#3AC7FF")
        border_color.setAlpha(255 if self.underMouse() else 120)
        painter.setPen(QPen(border_color, 2 if self.underMouse() else 1.3))
        painter.drawPath(path)

        # Ícono
        pixmap = QPixmap(self.icon_path if self.icon_path and os.path.exists(self.icon_path) else "assets/icons/default.png")
        if not pixmap.isNull():
            scaled = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            x = (self.width() - scaled.width()) / 2
            y = (self.height() - scaled.height()) / 2
            painter.drawPixmap(int(x), int(y), scaled)
