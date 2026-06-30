import sys
import win_magnification as mag
import keyboard
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import QTimer

app = QApplication(sys.argv)

# Inicializar magnification en el hilo principal
mag.initialize()

# Usamos flags para comunicar entre hilos
zoom_flag = {"zoom_in": False, "zoom_out": False}

# Hotkeys en hilo de keyboard (solo cambian flags)
keyboard.add_hotkey("z", lambda: zoom_flag.update({"zoom_in": True}))
keyboard.add_hotkey("x", lambda: zoom_flag.update({"zoom_out": True}))

# Timer de Qt en el hilo principal que revisa flags
def check_flags():
    if zoom_flag["zoom_in"]:
        mag.set_fullscreen_transform(2.0, (0,0))
        zoom_flag["zoom_in"] = False
    if zoom_flag["zoom_out"]:
        mag.reset_fullscreen_transform()
        zoom_flag["zoom_out"] = False

timer = QTimer()
timer.timeout.connect(check_flags)
timer.start(100)  # cada 100ms revisa

label = QLabel("Presiona Z para zoom, X para reset")
label.show()

sys.exit(app.exec())
