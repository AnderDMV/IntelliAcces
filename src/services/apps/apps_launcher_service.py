import os
import subprocess
from src.domain.models.app_info import AppInfo

class AppLauncherService:
    """
    Service responsible for launching applications.
    Does not handle UI or configuration, only execution.
    """

    # ==========================================================
    # Public API
    # ==========================================================

    def launch(self, app: AppInfo) -> bool:
        # Launches the given application (returns True if successful)
        if not self._is_valid_app(app):
            return False
        return self._execute(app.exe_path)

    # ==========================================================
    # Private methods
    # ==========================================================

    def _is_valid_app(self, app: AppInfo) -> bool:
        # Validates that the app has a valid executable path
        if not app or not app.exe_path:
            return False
        return os.path.exists(app.exe_path)

    def _execute(self, exe_path: str) -> bool:
        # Executes the application using subprocess
        try:
            subprocess.Popen(exe_path, shell=True)
            return True
        except Exception:
            return False
