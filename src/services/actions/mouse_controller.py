# mouse_controller.py
import pyautogui

class MouseController:

    def __init__(self):
        pyautogui.PAUSE = 0 

    def move_to(self, x, y, duration=0):
        pyautogui.moveTo(x, y, duration=duration)

    def click_at(self, x, y):
        pyautogui.click(x, y)

