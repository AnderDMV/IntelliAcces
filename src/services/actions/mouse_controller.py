# mouse_controller.py
from src.domain.interfaces.i_mouse_controller import IMouseController
import pyautogui

class MouseController(IMouseController):
    """
        Control the mouse by moving the cursor to click action.
    """

    def __init__(self):
        pyautogui.PAUSE = 0 

    def move_to(self, x, y, duration=0):
        """
        Move the cursor to a screen position specified by x and y coordinates.

        Args:
            x (int): x-coordinate
            y (int): y-coordinate
            duration (int): Duration of the mouse movement to the position (0 for the default camera)
        """
        pyautogui.moveTo(x, y, duration=duration)

    def click_at(self, x, y):
        """
        Move the cursor to a screen position specified by x and y coordinates.

        Args:
            x (int): x-coordinate
            y (int): y-coordinate
        """
        pyautogui.click(x, y)

