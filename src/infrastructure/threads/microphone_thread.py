from typing import Callable
import numpy as np
from PySide6.QtCore import QThread, QObject, Signal
import time

from src.domain.interfaces.i_camera_source import ICameraSource


class _Worker(QObject):
    
    pass


class MicrophoneThread:
    pass