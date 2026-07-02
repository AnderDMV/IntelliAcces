from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGraphicsDropShadowEffect
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QBrush,
    QFont,
    QLinearGradient,
    QPainterPath,
    QPolygonF
)
from PySide6.QtCore import Qt, Signal, QRectF, QPointF


class HomeView(QWidget):
    calibration_clicked = Signal()
    camera_state_clicked = Signal()
    apps_clicked = Signal()

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.topPanel = HomeTopBar()
        self.centerPanel = CenterPanel()

        main_layout.addWidget(self.topPanel)
        main_layout.addWidget(self.centerPanel)

        self.setLayout(main_layout)

        self.centerPanel.button_calibration.clicked.connect(self.calibration_clicked)
        self.centerPanel.button_camera_state.clicked.connect(self.camera_state_clicked)
        self.centerPanel.button_apps.clicked.connect(self.apps_clicked)


class HomeTopBar(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedHeight(88)
        self.setObjectName("homeTopBar")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setStyleSheet("""
            #homeTopBar {
                background-color: #0B1220;
                border-bottom: 1px solid rgba(255, 255, 255, 35);
            }

            QLabel {
                background-color: transparent;
            }

            QLabel#appTitle {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }

            QLabel#appSubtitle {
                color: #5CE1FF;
                font-size: 11px;
            }

            QLabel#logo {
                color: #5CE1FF;
                border: 2px solid #3AC7FF;
                border-radius: 19px;
                font-size: 18px;
                font-weight: bold;
                background-color: rgba(92, 225, 255, 25);
            }

            QPushButton {
                background-color: rgba(255, 255, 255, 18);
                color: white;
                border: none;
                border-radius: 17px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: rgba(92, 225, 255, 45);
            }

            QPushButton:pressed {
                background-color: rgba(92, 225, 255, 70);
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(10)

        logo = QLabel("⊙")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignCenter)
        logo.setFixedSize(40, 40)

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        title = QLabel("IntelliAccess")
        title.setObjectName("appTitle")

        subtitle = QLabel("Accesibilidad Inteligente")
        subtitle.setObjectName("appSubtitle")

        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        btn_theme = QPushButton("☼")
        btn_theme.setFixedSize(42, 34)

        btn_settings = QPushButton("⚙")
        btn_settings.setFixedSize(42, 34)

        btn_minimize = QPushButton("–")
        btn_minimize.setFixedSize(42, 34)
        btn_minimize.clicked.connect(lambda: self.window().showMinimized())

        btn_close = QPushButton("×")
        btn_close.setFixedSize(42, 34)
        btn_close.clicked.connect(lambda: self.window().close())

        layout.addWidget(logo)
        layout.addLayout(text_layout)
        layout.addStretch()
        
        layout.addSpacing(6)
        layout.addWidget(btn_minimize)
        layout.addWidget(btn_close)

        self.setLayout(layout)


class CenterPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("centerPanel")
        self.setAttribute(Qt.WA_StyledBackground, True)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(18, 28, 18, 24)
        main_layout.setSpacing(0)

        title = QLabel("¡Bienvenido! 👋")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #5CE1FF;
                font-size: 28px;
                font-weight: bold;
                background-color: transparent;
            }
        """)

        subtitle = QLabel("")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                color: #B8C2D6;
                font-size: 14px;
                background-color: transparent;
            }
        """)

        cards_layout = QHBoxLayout()
        cards_layout.setContentsMargins(0, 24, 0, 0)
        cards_layout.setSpacing(8)

        self.button_calibration = AccessCardButton(
            title="Calibrar",
            subtitle="Calibración del head\nTracking",
            action_text="Calibrar",
            card_type="microphone",
            accent_1="#5CE1FF",
            accent_2="#58D7E7"
        )

        self.button_camera_state = AccessCardButton(
            title="Estado de la\ncaptura",
            subtitle="Ver el estado de\nla captura de video",
            action_text="Abrir",
            card_type="star",
            accent_1="#5D78FF",
            accent_2="#7246FF"
        )

        self.button_apps = AccessCardButton(
            title="Aplicaciones",
            subtitle="Accede a tus apps\nfavoritas",
            action_text="Ver todas",
            card_type="apps",
            accent_1="#8E44FF",
            accent_2="#6226D9"
        )

        for button in (
            self.button_calibration,
            self.button_camera_state,
            self.button_apps
        ):
            self.add_shadow(button)

        cards_layout.addStretch()
        cards_layout.addWidget(self.button_calibration)
        cards_layout.addWidget(self.button_camera_state)
        cards_layout.addWidget(self.button_apps)
        cards_layout.addStretch()

        main_layout.addWidget(title)
        main_layout.addSpacing(8)
        main_layout.addWidget(subtitle)
        main_layout.addStretch()
        main_layout.addLayout(cards_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()

        gradient = QLinearGradient(0, 0, rect.width(), rect.height())
        gradient.setColorAt(0.0, QColor("#07111F"))
        gradient.setColorAt(0.45, QColor("#101831"))
        gradient.setColorAt(1.0, QColor("#080A18"))

        painter.fillRect(rect, gradient)

        painter.setPen(QPen(QColor(92, 225, 255, 24), 1))

        for x in range(35, rect.width(), 28):
            for y in range(25, rect.height(), 28):
                painter.drawPoint(x, y)

        painter.setPen(QPen(QColor(61, 118, 255, 55), 2))
        painter.drawEllipse(QPointF(-35, 175), 165, 165)
        painter.drawEllipse(QPointF(rect.width() + 20, rect.height() - 60), 150, 150)

        painter.setPen(QPen(QColor(132, 55, 255, 45), 1))
        painter.drawEllipse(QPointF(rect.width() - 20, rect.height() - 30), 110, 110)

        super().paintEvent(event)

    def add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 90))
        widget.setGraphicsEffect(shadow)


class AccessCardButton(QPushButton):
    def __init__(
        self,
        title,
        subtitle,
        action_text,
        card_type,
        accent_1,
        accent_2
    ):
        super().__init__()

        self.title = title
        self.subtitle = subtitle
        self.action_text = action_text
        self.card_type = card_type
        self.accent_1 = QColor(accent_1)
        self.accent_2 = QColor(accent_2)

        self.setFixedSize(180, 265)
        self.setCursor(Qt.PointingHandCursor)
        self.setMouseTracking(True)
        self.setText("")
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
        """)

    def enterEvent(self, event):
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.isDown():
            painter.translate(1.5, 2)

        w = self.width()
        h = self.height()

        card_rect = QRectF(4, 4, w - 8, h - 8)

        card_path = QPainterPath()
        card_path.addRoundedRect(card_rect, 18, 18)

        card_gradient = QLinearGradient(0, 0, 0, h)
        card_gradient.setColorAt(0.0, QColor(26, 44, 70, 235))
        card_gradient.setColorAt(1.0, QColor(13, 21, 43, 245))

        painter.fillPath(card_path, card_gradient)

        border_color = QColor(self.accent_1)
        border_color.setAlpha(245 if self.underMouse() else 150)

        painter.setPen(QPen(border_color, 2 if self.underMouse() else 1.3))
        painter.drawPath(card_path)

        glow_color = QColor(self.accent_1)
        glow_color.setAlpha(26)
        painter.setBrush(QBrush(glow_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(w / 2, 64), 48, 48)

        icon_circle = QRectF((w - 76) / 2, 28, 76, 76)

        circle_gradient = QLinearGradient(
            icon_circle.left(),
            icon_circle.top(),
            icon_circle.right(),
            icon_circle.bottom()
        )
        circle_gradient.setColorAt(0.0, QColor(255, 255, 255, 22))
        circle_gradient.setColorAt(1.0, QColor(255, 255, 255, 5))

        circle_path = QPainterPath()
        circle_path.addEllipse(icon_circle)

        painter.fillPath(circle_path, circle_gradient)

        icon_border = QColor(self.accent_1)
        icon_border.setAlpha(95)
        painter.setPen(QPen(icon_border, 1.4))
        painter.drawEllipse(icon_circle)

        if self.card_type == "microphone":
            self.drac_refactor_icon(painter, QPointF(w / 2, 66))
        elif self.card_type == "star":
            self.draw_camera_icon(painter, QPointF(w / 2, 66))
        else:
            self.draw_apps_icon(painter, QPointF(w / 2, 66))

        painter.setPen(QColor("#FFFFFF"))
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        painter.setFont(title_font)
        painter.drawText(QRectF(0, 124, w, 35), Qt.AlignCenter, self.title)

        painter.setPen(QColor("#B8C2D6"))
        subtitle_font = QFont()
        subtitle_font.setPointSize(8)
        painter.setFont(subtitle_font)
        painter.drawText(
            QRectF(10, 158, w - 20, 44),
            Qt.AlignCenter,
            self.subtitle
        )

        button_rect = QRectF(18, h - 54, w - 36, 34)
        button_path = QPainterPath()
        button_path.addRoundedRect(button_rect, 17, 17)

        button_gradient = QLinearGradient(
            button_rect.left(),
            button_rect.top(),
            button_rect.right(),
            button_rect.bottom()
        )
        button_gradient.setColorAt(0.0, self.accent_1)
        button_gradient.setColorAt(1.0, self.accent_2)

        painter.fillPath(button_path, button_gradient)

        painter.setPen(QColor("#FFFFFF"))
        action_font = QFont()
        action_font.setPointSize(9)
        action_font.setBold(True)
        painter.setFont(action_font)
        painter.drawText(button_rect, Qt.AlignCenter, self.action_text + "   ›")

    def drac_refactor_icon(self, painter, center):
        painter.setPen(QPen(QColor("#FFD447"), 3))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QRectF(center.x() - 18, center.y() - 18, 36, 36))
        painter.drawLine(center.x(), center.y() - 18, center.x(), center.y() + 18)
        painter.drawLine(center.x() - 18, center.y(), center.x() + 18, center.y())

    def draw_camera_icon(self, painter, center):
        body = QRectF(center.x() - 20, center.y() - 12, 40, 24)
        painter.setBrush(QBrush(QColor("#5CE1FF")))
        painter.setPen(QPen(QColor("#3AC7FF"), 2))
        painter.drawRoundedRect(body, 6, 6)
        lens = QRectF(center.x() - 8, center.y() - 8, 16, 16)
        painter.setBrush(QBrush(QColor("#101831")))
        painter.drawEllipse(lens)

    def draw_apps_icon(self, painter, center):
        size = 17
        gap = 8

        start_x = center.x() - size - gap / 2
        start_y = center.y() - size - gap / 2

        colors = [
            QColor("#FFD447"),
            QColor("#4A7DFF"),
            QColor("#FF3F3F"),
            QColor("#5CE1FF"),
        ]

        positions = [
            (start_x, start_y),
            (start_x + size + gap, start_y),
            (start_x, start_y + size + gap),
            (start_x + size + gap, start_y + size + gap),
        ]

        painter.setPen(Qt.NoPen)

        for i, position in enumerate(positions):
            painter.setBrush(QBrush(colors[i]))
            painter.drawRoundedRect(
                QRectF(position[0], position[1], size, size),
                5,
                5
            )

        painter.setPen(QPen(self.accent_1, 3))
        painter.drawLine(
            QPointF(center.x() + 31, center.y() + 17),
            QPointF(center.x() + 31, center.y() + 37)
        )
        painter.drawLine(
            QPointF(center.x() + 21, center.y() + 27),
            QPointF(center.x() + 41, center.y() + 27)
        )