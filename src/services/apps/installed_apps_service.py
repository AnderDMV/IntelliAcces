import os
import winreg
import win32com.client
from src.domain.models.app_info import AppInfo

class InstalledAppsService:
    def __init__(self):
        self._apps_cache: list[AppInfo] = []
        self._cache_loaded = False

    def get_apps(self) -> list[AppInfo]:
        if not self._cache_loaded:
            self.refresh()
        return self._apps_cache.copy()

    def refresh(self) -> list[AppInfo]:
        apps = self._discover_apps()
        self._sort_apps(apps)
        self._apps_cache = apps
        self._cache_loaded = True
        return self._apps_cache.copy()

    def _discover_apps(self) -> list[AppInfo]:
        apps = []
        shell = win32com.client.Dispatch("WScript.Shell")

        # 1. Buscar accesos directos SOLO en el menú inicio
        start_menu_paths = [
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
            os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs")
        ]

        for path in start_menu_paths:
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".lnk"):
                        try:
                            shortcut = shell.CreateShortcut(os.path.join(root, file))
                            exe_path = shortcut.Targetpath

                            if exe_path:
                                app_name = os.path.splitext(file)[0]

                                # Construir ruta del icono esperado
                                icon_candidate = os.path.join("assets", "appsIcons", f"{app_name}.png")
                                icon_path = icon_candidate if os.path.exists(icon_candidate) else "assets/icons/default.png"

                                apps.append(AppInfo(
                                    name=app_name,
                                    exe_path=exe_path,
                                    icon_path=icon_path
                                ))
                        except Exception as e:
                            print(f"Error procesando acceso directo {file}: {e}")

        # 2. Fallback: usar el registro si no se encontró nada
        if not apps:
            reg_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
            ]
            for hive, path in reg_paths:
                try:
                    with winreg.OpenKey(hive, path) as key:
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    exe_path = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                    if name and exe_path:
                                        icon_candidate = os.path.join("assets", "appsIcons", f"{name}.png")
                                        icon_path = icon_candidate if os.path.exists(icon_candidate) else "assets/icons/default.png"

                                        apps.append(AppInfo(
                                            name=name,
                                            exe_path=exe_path,
                                            icon_path=icon_path
                                        ))
                                except FileNotFoundError:
                                    continue
                except Exception:
                    continue

        return apps

    def _sort_apps(self, apps: list[AppInfo]):
        apps.sort(key=lambda app: app.name.lower())
