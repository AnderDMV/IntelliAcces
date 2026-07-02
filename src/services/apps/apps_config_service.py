import json
from pathlib import Path
from src.domain.models.app_info import AppInfo

class AppsConfigService:
    TOTAL_SLOTS = 9  # Fixed number of grid slots

    def __init__(self, config_path: str = "config/apps.json"):
        self._config_path = Path(config_path)
        self._create_config_if_not_exists()

    # ==========================
    # Public
    # ==========================

    def load_slots(self) -> list[AppInfo | None]:
        """
        Returns a list of slots (length = TOTAL_SLOTS).
        Each slot contains either an AppInfo or None.
        """
        data = self._read_json()
        slots: list[AppInfo | None] = []

        for item in data:
            if item is None:
                slots.append(None)
            else:
                slots.append(
                    AppInfo(
                        name=item["name"],
                        exe_path=item["exe_path"],
                        icon_path=item.get("icon_path") or "assets/icons/default.png"
                    )
                )
        return slots

    def assign_app(self, slot: int, app: AppInfo):
        # Assigns an app to a specific slot
        self._validate_slot(slot)
        slots = self.load_slots()
        slots[slot] = app
        self._write_slots(slots)

    def remove_app(self, slot: int):
        # Removes an app from a specific slot
        self._validate_slot(slot)
        slots = self.load_slots()
        slots[slot] = None
        self._write_slots(slots)

    # ==========================
    # Private
    # ==========================

    def _create_config_if_not_exists(self):
        # Ensures config file exists with empty slots
        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._config_path.exists():
            with self._config_path.open("w", encoding="utf-8") as file:
                json.dump([None] * self.TOTAL_SLOTS, file, indent=4, ensure_ascii=False)

    def _read_json(self):
        # Reads JSON config file
        with self._config_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _write_slots(self, slots: list[AppInfo | None]):
        # Writes slots back to JSON file
        data = []
        for app in slots:
            if app is None:
                data.append(None)
            else:
                data.append({
                    "name": app.name,
                    "exe_path": app.exe_path,
                    "icon_path": app.icon_path
                })
        with self._config_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def _validate_slot(self, slot: int):
        # Validates slot index is within range
        if not 0 <= slot < self.TOTAL_SLOTS:
            raise ValueError(f"Invalid slot: {slot}")
