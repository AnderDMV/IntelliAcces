from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
    QHBoxLayout,
    QPushButton
)

from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QLinearGradient,
    QPainterPath,
    QPixmap
)

from PySide6.QtCore import Qt, Signal, QRectF

from src.presentation.widgets.ip_buttons import IntelliButton


class AppsView(QWidget):

    add_apps_clicked = Signal()
    back_clicked = Signal()
    open_app_clicked = Signal(str, str, str)

    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_StyledBackground, True)

#MAIN LAYOUT

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(28, 28, 28, 28)
        main_layout.setSpacing(18)

#CABEZA
        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()

        title = QLabel("Aplicaciones")
        title.setStyleSheet("""
            QLabel{
                color: #5CE1FF;
                font-size: 28px;
                font-weight: bold;
                background: transparent;
            }
        """)

        subtitle = QLabel("Selecciona o agrega una aplicación")
        subtitle.setStyleSheet("""
            QLabel{
                color: #B8C2D6;
                font-size: 15px;
                background: transparent;
            }
        """)

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

#ADD BOTON

        add_apps_button = IntelliButton("+")
        add_apps_button.setFixedSize(70, 70)

        add_apps_button.setStyleSheet("""
            QPushButton{
                background-color: rgba(255,255,255,18);
                border: 2px solid #3AC7FF;
                border-radius: 35px;
                color: white;
                font-size: 28px;
                font-weight: bold;
            }

            QPushButton:hover{
                background-color: rgba(92,225,255,40);
            }
        """)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(add_apps_button)

#GRID

        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(18)
        grid_layout.setVerticalSpacing(18)
        grid_layout.setSpacing(18)

        apps = [
        ("Chrome", "assets/icons/cromo.png"),
        ("WhatsApp", "assets/icons/whatsapp.png"),
        ("Word", "assets/icons/archivo-de-word.png"),
        ("Adjunto", "assets/icons/adjunto-archivo.png"),
        ("+", "assets/icons/signo-de-mas.png"),
        ("+", "assets/icons/signo-de-mas.png"),
        ("+", "assets/icons/signo-de-mas.png"),
        ("+", "assets/icons/signo-de-mas.png"),
        ("+", "assets/icons/signo-de-mas.png"),]

        index = 0

        cardList = []
        for fila in range(3):
            for columna in range(3):
                title, icon = apps[index]
                card = AppCard(title, icon)
                cardList.append(card)
                grid_layout.addWidget(card, fila, columna)
                index += 1
#BOTON

        back_button = IntelliButton("←  Volver")
        back_button.setFixedHeight(60)

        back_button.setStyleSheet("""
            QPushButton{
                background-color: rgba(255,255,255,14);
                border: 2px solid #3AC7FF;
                border-radius: 24px;
                color: white;
                font-size: 24px;
                font-weight: bold;
            }

            QPushButton:hover{
                background-color: rgba(92,225,255,40);
            }
        """)

#ADD EVERYTHING

        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        grid_container = QWidget()
        grid_container.setStyleSheet("""
        background: transparent;""")
        grid_container.setLayout(grid_layout)

        grid_wrapper = QHBoxLayout()
        grid_wrapper.addStretch()
        grid_wrapper.addWidget(grid_container)
        grid_wrapper.addStretch()

        main_layout.addLayout(grid_wrapper)
        main_layout.addSpacing(10)
        main_layout.addWidget(back_button)

        self.setLayout(main_layout)

#CONECCIONES
        add_apps_button.clicked.connect(self.add_apps_clicked)
        back_button.clicked.connect(self.back_clicked)

        for card in cardList:
            self.app_title = card.get_title()
            self.app_path = card.get_path()
            self.app_icon_path = card.get_icon_path()
            card.clicked.connect(self._open_emisor)


#BACKGROUND
    def _open_emisor(self):
        self.open_app_clicked.emit( self.app_path, self.app_title, self.app_icon_path)

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()

        gradient = QLinearGradient(
            0,
            0,
            rect.width(),
            rect.height()
        )

        gradient.setColorAt(0.0, QColor("#07111F"))
        gradient.setColorAt(0.45, QColor("#101831"))
        gradient.setColorAt(1.0, QColor("#080A18"))

        painter.fillRect(rect, gradient)

        painter.setPen(QPen(QColor(92, 225, 255, 24), 1))

        for x in range(35, rect.width(), 28):
            for y in range(25, rect.height(), 28):
                painter.drawPoint(x, y)

        super().paintEvent(event)


#CARD

class AppCard(QPushButton):

    def __init__(self, title, icon_path):
        self.app_path = ""
        self.icon_path = icon_path
        super().__init__()

        self.title = title

        self.setFixedSize(130, 130)

        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet("""
            QPushButton{
                background: transparent;
                border: none;
            }
        """)
    
    def get_path(self):
        return self.app_path

    def get_icon_path(self):
        return self.icon_path
    
    def get_title(self):
        return self.title

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

        painter.setPen(
            QPen(
                border_color,
                2 if self.underMouse() else 1.3
            )
        )
        painter.drawPath(path)

        pixmap = QPixmap(self.icon_path)

        if not pixmap.isNull():

            scaled = pixmap.scaled(
                64,
                64,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            x = (self.width() - scaled.width()) / 2
            y = (self.height() - scaled.height()) / 2

            painter.drawPixmap(int(x), int(y), scaled)

