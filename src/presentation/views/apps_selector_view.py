import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPixmap, QColor, QPainter, QPen, QLinearGradient, QPainterPath
from PySide6.QtCore import Qt, Signal, QRectF
from src.domain.models.app_info import AppInfo

class AppsSelectorView(QWidget):
    exit_clicked = Signal()
    app_selected = Signal(AppInfo)

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Layout principal
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(28, 28, 28, 28)
        self.main_layout.setSpacing(28)

        # Encabezado
        header_layout = QHBoxLayout()
        title = QLabel("Selector de Aplicaciones")
        title.setStyleSheet("color: #5CE1FF; font-size: 30px; font-weight: bold; background: transparent;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        exit_button = QPushButton("← Volver")
        exit_button.setFixedHeight(100)
        exit_button.setStyleSheet(
            "background-color: rgba(255,255,255,14); "
            "border: 2px solid #3AC7FF; border-radius: 24px; "
            "padding: 0 28px; "  # más espacio interno
            "color: white; font-size: 22px; font-weight: bold;"
        )
        exit_button.clicked.connect(self.exit_clicked)
        header_layout.addWidget(exit_button)

        self.main_layout.addLayout(header_layout)

        # Área de app seleccionada
        app_area = QVBoxLayout()
        app_area.setSpacing(12)

        self.app_label = QLabel("No apps loaded")
        self.app_label.setAlignment(Qt.AlignCenter)
        self.app_label.setStyleSheet("color: #B8C2D6; font-size: 24px; font-weight: bold; background: transparent;")
        app_area.addWidget(self.app_label)

        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)
        app_area.addWidget(self.icon_label)

        self.main_layout.addLayout(app_area)

        # Botones de navegación
        nav_layout = QHBoxLayout()
        self.prev_button = NavButton("← Anterior")
        self.confirm_button = NavButton("Confirmar")
        self.next_button = NavButton("Siguiente →")

        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.confirm_button)
        nav_layout.addWidget(self.next_button)

        self.main_layout.addLayout(nav_layout)
        self.setLayout(self.main_layout)

        # Estado interno
        self.apps: list[AppInfo] = []
        self.current_index = 0

        # Conexiones
        self.prev_button.clicked.connect(self._show_previous)
        self.next_button.clicked.connect(self._show_next)
        self.confirm_button.clicked.connect(self._confirm_selection)

    def load_apps(self, apps: list[AppInfo]):
        self.apps = apps
        self.current_index = 0
        if self.apps:
            self._show_app(self.apps[0])

    def _show_app(self, app: AppInfo):
        self.app_label.setText(app.name)
        icon_path = app.icon_path if app.icon_path and os.path.exists(app.icon_path) else "assets/icons/app.png"
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            # Ícono original de 96px, centrado y cercano al nombre
            self.icon_label.setPixmap(
                pixmap.scaled(96, 96, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )

    def _show_previous(self):
        if self.apps:
            self.current_index = (self.current_index - 1) % len(self.apps)
            self._show_app(self.apps[self.current_index])

    def _show_next(self):
        if self.apps:
            self.current_index = (self.current_index + 1) % len(self.apps)
            self._show_app(self.apps[self.current_index])

    def _confirm_selection(self):
        if self.apps:
            self.app_selected.emit(self.apps[self.current_index])


class NavButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedSize(180, 130)  # más grandes y cuadrados
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("background: transparent; border: none; font-size: 22px; font-weight: bold; color: white;")

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

        # Texto centrado
        painter.setPen(QColor("white"))
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignCenter, self.text())
