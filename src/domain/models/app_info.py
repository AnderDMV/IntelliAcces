from dataclasses import dataclass


@dataclass(slots=True)
class AppInfo:
    name: str
    exe_path: str
    icon_path: str