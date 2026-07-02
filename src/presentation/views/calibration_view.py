from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QIcon, QImage, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt, QSize, Signal

from src.presentation.widgets.ip_buttons import IntelliButton


class CalibrationView(QWidget):
    confirm_clicked = Signal()
    recalibrate_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setContentsMargins(30, 30, 30, 30)

        # Main layout
        pMainLayout = QVBoxLayout()
        pMainLayout.setSpacing(28)

        self.setStyleSheet("background-color: #101831;")


        # Sections
        self._create_header(pMainLayout)
        self._create_center_section(pMainLayout)
        self._create_footer(pMainLayout)

        self.setLayout(pMainLayout)

    # -------------------------------
    # Header
    def _create_header(self, layout):
        header_label = QLabel("Calibración")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            color: #5CE1FF;
            font-size: 30px;
            font-weight: bold;
            background-color: transparent;
        """)
        layout.addWidget(header_label)

        subtitle = QLabel("Sigue las instrucciones para completar la calibración")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            color: #B8C2D6;
            font-size: 14px;
            background-color: transparent;
        """)
        layout.addWidget(subtitle)

    # -------------------------------
    # Center section divided in two parts
    def _create_center_section(self, layout):
        center_layout = QHBoxLayout()

        # Left side: camera + face state
        left_layout = QVBoxLayout()
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        # Face state
        state_layout = QHBoxLayout()
        self.face_icon = QLabel()
        self.face_icon.setFixedSize(40, 40)
        self.face_state_label = QLabel("Rostro no detectado")
        self.face_state_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FF3F3F;")
        state_layout.addWidget(self.face_icon)
        state_layout.addWidget(self.face_state_label)

        left_layout.addWidget(self.label)
        left_layout.addLayout(state_layout)

        # Right side: instructions + images
        right_layout = QVBoxLayout()
        instr_label = QLabel("Mira al centro de la pantalla y parpadea")
        instr_label.setAlignment(Qt.AlignCenter)
        instr_label.setStyleSheet("""
            color: #B8C2D6;
            font-size: 18px;
            font-weight: bold;
            background-color: transparent;
        """)

        images_layout = QHBoxLayout()
        self.eye_img = QLabel()
        self.eye_img.setPixmap(QPixmap("assets/icons/eye.png").scaled(100, 100, Qt.KeepAspectRatio))
        self.monitor_img = QLabel()
        self.monitor_img.setPixmap(QPixmap("assets/icons/monitor.png").scaled(100, 100, Qt.KeepAspectRatio))

        images_layout.addWidget(self.eye_img)
        images_layout.addWidget(self.monitor_img)

        right_layout.addWidget(instr_label)
        right_layout.addLayout(images_layout)

        center_layout.addLayout(left_layout)
        center_layout.addLayout(right_layout)

        layout.addLayout(center_layout)

    # -------------------------------
    # Footer with confirmation
    def _create_footer(self, layout):
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignCenter)
        footer_layout.setSpacing(40)

        # Confirmation button
        self.confirm_button = IntelliButton("Confirmar calibración")
        self.confirm_button.setIcon(QIcon("assets/icons/check.png"))
        self.confirm_button.setIconSize(QSize(50, 50))
        self.confirm_button.setFixedWidth(240)

        # Recalibrate button
        self.recalibrate_button = IntelliButton("Recalibrar")
        self.recalibrate_button.setIcon(QIcon("assets/icons/refresh.png"))
        self.recalibrate_button.setIconSize(QSize(50, 50))
        self.recalibrate_button.setFixedWidth(240)

        footer_layout.addWidget(self.confirm_button)
        footer_layout.addWidget(self.recalibrate_button)

        layout.addLayout(footer_layout)

        # Connect internal signals
        self.confirm_button.clicked.connect(self.confirm_clicked)
        self.recalibrate_button.clicked.connect(self.recalibrate_clicked)

    # -------------------------------
    # Update methods (called externally)
    def update_frame(self, img, h, w, bytes_per_line):
        qimg = QImage(img, w, h, bytes_per_line, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qimg))

    def update_face_state(self, detected: bool):
        if hasattr(self, "_last_state") and self._last_state == detected:
            return
        self._last_state = detected

        if detected:
            self.face_icon.setPixmap(QPixmap("assets/icons/check.png").scaled(40, 40, Qt.KeepAspectRatio))
            self.face_state_label.setText("Rostro detectado")
            self.face_state_label.setStyleSheet("color: #5CE1FF; font-size: 20px; font-weight: bold;")
        else:
            self.face_icon.setPixmap(QPixmap("assets/icons/x.png").scaled(40, 40, Qt.KeepAspectRatio))
            self.face_state_label.setText("Rostro no detectado")
            self.face_state_label.setStyleSheet("color: #FF3F3F; font-size: 20px; font-weight: bold;")

    def confirm_calibration(self):
        self.face_state_label.setText("Calibración exitosa")
        self.face_state_label.setStyleSheet("color: #5CE1FF; font-size: 20px; font-weight: bold;")

    # -------------------------------
    # Fondo único aplicado
    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        painter.fillRect(rect, QColor("#101831"))  # color único de fondo
        super().paintEvent(event)
