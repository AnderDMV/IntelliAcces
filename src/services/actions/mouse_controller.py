# mouse_controller.py
import pyautogui

class MouseController:
    """Controlador de mouse usando PyAutoGUI"""

    def __init__(self):
        # Opcional: puedes configurar la pausa entre acciones
        pyautogui.PAUSE = 0  # sin pausa, ejecución inmediata

    def move_to(self, x, y, duration=0):
        """
        Mueve el cursor a las coordenadas (x, y).
        duration controla la velocidad del movimiento (0 = instantáneo).
        """
        pyautogui.moveTo(x, y, duration=duration)

    def click_at(self, x, y):
        """
        Hace clic izquierdo en las coordenadas (x, y).
        """
        pyautogui.click(x, y)


if __name__ == "__main__":
    mc = MouseController()
    # Ejemplo: clic en (100, 200)
    mc.click_at(100, 200)
    # Luego mover el cursor a (0, 0) para "ocultarlo"
    mc.move_to(0, 0)
