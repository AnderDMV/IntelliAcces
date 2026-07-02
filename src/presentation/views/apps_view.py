import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtGui import QColor, QPainter, QPen, QLinearGradient, QPainterPath, QPixmap
from PySide6.QtCore import Qt, Signal, QRectF
from src.domain.models.app_info import AppInfo
from src.presentation.widgets.slot_chooser_dialog import SlotChooserDialog  # import aquí

class AppsView(QWidget):
    add_apps_clicked = Signal(int)   # slot vacío
    add_new_app_clicked = Signal(int)  # botón superior ahora emite índice elegido
    back_clicked = Signal()
    open_app_clicked = Signal(str, str, str)

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(28, 28, 28, 28)
        self.main_layout.setSpacing(18)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Aplicaciones")
        title.setStyleSheet("color: #5CE1FF; font-size: 28px; font-weight: bold; background: transparent;")
        subtitle = QLabel("Selecciona o agrega una aplicación")
        subtitle.setStyleSheet("color: #B8C2D6; font-size: 15px; background: transparent;")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.addStretch()

        # Botón extra para añadir app (arriba de la rejilla)
        new_app_button = QPushButton("➕ Añadir aplicación")
        new_app_button.setFixedHeight(60)
        new_app_button.setStyleSheet(
            "background-color: rgba(255,255,255,14); "
            "border: 2px solid #3AC7FF; border-radius: 24px; "
            "color: white; font-size: 20px; font-weight: bold;"
        )
        new_app_button.clicked.connect(self._open_slot_chooser)

        # Grid layout for apps
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(18)

        # Back button
        back_button = QPushButton("← Volver")
        back_button.setFixedHeight(60)
        back_button.setStyleSheet(
            "background-color: rgba(255,255,255,14); "
            "border: 2px solid #3AC7FF; border-radius: 24px; "
            "color: white; font-size: 24px; font-weight: bold;"
        )
        back_button.clicked.connect(self.back_clicked)

        # Assemble layout
        self.main_layout.addLayout(header_layout)
        self.main_layout.addWidget(new_app_button)   # botón arriba de la rejilla
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addWidget(back_button)
        self.setLayout(self.main_layout)

    def populate_grid(self, slots: list[AppInfo | None]):
        # Clears previous grid before repopulating
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Builds grid dynamically from slots
        index = 0
        for row in range(3):
            for col in range(3):
                app = slots[index]
                if app is None:
                    card = AppCard("+", "assets/icons/signo-de-mas.png")
                    card.clicked.connect(lambda _, i=index: self.add_apps_clicked.emit(i))
                else:
                    card = AppCard(app.name, app.icon_path)
                    card.app_path = app.exe_path
                    card.clicked.connect(lambda _, a=app: self.open_app_clicked.emit(a.exe_path, a.name, a.icon_path))
                self.grid_layout.addWidget(card, row, col)
                index += 1

    def _open_slot_chooser(self):
        dialog = SlotChooserDialog(self)
        if dialog.exec():
            chosen_slot = dialog.chosen_slot
            if chosen_slot is not None:
                self.add_new_app_clicked.emit(chosen_slot)

class AppCard(QPushButton):
    def __init__(self, title, icon_path):
        super().__init__()
        self.title = title
        self.icon_path = icon_path
        self.app_path = ""
        self.setFixedSize(130, 130)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("background: transparent; border: none;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(4, 4, self.width()-8, self.height()-8)
        path = QPainterPath()
        path.addRoundedRect(rect, 20, 20)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(26, 44, 70, 235))
        gradient.setColorAt(1.0, QColor(13, 21, 43, 245))
        painter.fillPath(path, gradient)

        border_color = QColor("#3AC7FF")
        border_color.setAlpha(255 if self.underMouse() else 120)
        painter.setPen(QPen(border_color, 2 if self.underMouse() else 1.3))
        painter.drawPath(path)

        pixmap = QPixmap(self.icon_path if self.icon_path and os.path.exists(self.icon_path) else "assets/icons/default.png")
        if not pixmap.isNull():
            scaled = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            x = (self.width() - scaled.width()) / 2
            y = (self.height() - scaled.height()) / 2
            painter.drawPixmap(int(x), int(y), scaled)
