from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QIcon, QImage, QPixmap
from PySide6.QtCore import Qt, QSize, Signal

from src.presentation.widgets.ip_buttons import IntelliButton


class CalibrationView(QWidget):
    # Internal signal for confirmation button
    confirm_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setContentsMargins(30, 30, 30, 30)

        # Main layout
        pMainLayout = QVBoxLayout()
        pMainLayout.setSpacing(20)

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
        header_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(header_label)

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
        self.face_icon.setFixedSize(30, 30)
        self.face_state_label = QLabel("Rostro no detectado")
        state_layout.addWidget(self.face_icon)
        state_layout.addWidget(self.face_state_label)

        left_layout.addWidget(self.label)
        left_layout.addLayout(state_layout)

        # Right side: instructions + images
        right_layout = QVBoxLayout()
        instr_label = QLabel("Mira al centro de la pantalla y parpadea")
        instr_label.setAlignment(Qt.AlignCenter)
        instr_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        images_layout = QHBoxLayout()
        self.eye_img = QLabel()
        self.eye_img.setPixmap(QPixmap("assets/icons/monitor.png").scaled(100, 100, Qt.KeepAspectRatio))
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
        footer_layout = QVBoxLayout()
        footer_layout.setAlignment(Qt.AlignCenter)

        self.success_label = QLabel("Esperando calibración...")
        self.success_label.setAlignment(Qt.AlignCenter)
        self.success_label.setStyleSheet("font-size: 16px;")

        # Confirmation button
        self.confirm_button = IntelliButton()
        self.confirm_button.setIcon(QIcon("assets/icons/check.png"))
        self.confirm_button.setIconSize(QSize(50, 50))

        footer_layout.addWidget(self.success_label)
        footer_layout.addWidget(self.confirm_button)

        layout.addLayout(footer_layout)

        # Connect internal signal
        self.confirm_button.clicked.connect(self.confirm_clicked)

    # -------------------------------
    # Update methods (called externally)
    def update_frame(self, img, h, w, bytes_per_line):
        """Update camera frame in the left section"""
        qimg = QImage(img, w, h, bytes_per_line, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qimg))

    def update_face_state(self, detected: bool):
        """Update face detection state only when it changes"""
        if hasattr(self, "_last_state") and self._last_state == detected:
            return  # Skip update if state hasn't changed
        self._last_state = detected

        if detected:
            self.face_icon.setPixmap(QPixmap("assets/icons/check.png").scaled(30, 30, Qt.KeepAspectRatio))
            self.face_state_label.setText("Rostro detectado")
            self.face_state_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.face_icon.setPixmap(QPixmap("assets/icons/x.png").scaled(30, 30, Qt.KeepAspectRatio))
            self.face_state_label.setText("Rostro no detectado")
            self.face_state_label.setStyleSheet("color: red; font-weight: bold;")


    def confirm_calibration(self):
        """Update footer label when calibration is successful"""
        self.success_label.setText("Calibración exitosa. Presiona el botón para confirmar.")
