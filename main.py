import sys
from app import Application
from PySide6.QtWidgets import QApplication


def main():
    qt_app = QApplication(sys.argv)
    qt_app.setApplicationName("IntelliAcces")
    qt_app.setApplicationVersion("1.0.0")

    app = Application(qt_app)
    app.start()
    sys.exit(qt_app.exec())
    

if __name__ == "__main__":
    main()
