import os
import win32api
import win32gui
import win32con
from PIL import Image
from src.domain.models.app_info import AppInfo

class IconExtractor:
    @staticmethod
    def extract_icon(exe_path: str, save_path: str) -> str:
        """
        Extrae el primer ícono de un ejecutable y lo guarda como .ico en disco.
        Devuelve la ruta al archivo guardado o un ícono por defecto si falla.
        """
        try:
            large, small = win32gui.ExtractIconEx(exe_path, 0)
            if large:
                hicon = large[0]
                ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
                ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)

                hdc = win32gui.CreateCompatibleDC(0)
                hbm = win32gui.CreateCompatibleBitmap(hdc, ico_x, ico_y)
                hdc_old = win32gui.SelectObject(hdc, hbm)
                win32gui.DrawIconEx(hdc, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)

                # Convertir el bitmap a imagen PIL
                bmpinfo = win32gui.GetObject(hbm)
                bmpstr = win32gui.GetBitmapBits(hbm, True)
                img = Image.frombuffer(
                    "RGBA",
                    (bmpinfo.bmWidth, bmpinfo.bmHeight),
                    bmpstr, "raw", "BGRA", 0, 1
                )

                # Crear carpeta si no existe
                os.makedirs(os.path.dirname(save_path), exist_ok=True)

                # Guardar como .ico
                img.save(save_path, format="ICO")

                # Liberar recursos
                win32gui.SelectObject(hdc, hdc_old)
                win32gui.DeleteDC(hdc)
                win32gui.DestroyIcon(hicon)

                return save_path
        except Exception:
            return "assets/icons/default.png"
