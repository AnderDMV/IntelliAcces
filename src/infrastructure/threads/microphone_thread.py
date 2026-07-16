from typing import Callable
import numpy as np
from PySide6.QtCore import QThread, QObject, Signal
import time

from src.domain.interfaces.i_microphone_source import IMicrophoneSource
from src.domain.interfaces.i_voice_detector import IVoiceDetector


class _Worker(QObject):
    
    command_ready = Signal()
    
    def __init__(self, microphone: IMicrophoneSource, voice_detector: IVoiceDetector):
        super().__init__()
        self._microphone  = microphone
        self._voice_detector = voice_detector
        self._running = False

    def run(self) -> None:
        self._running = True
        try:
            self._microphone.start()
            while self._running:
                audio_block = self._microphone.read_audio()
                result = self._voice_detector.process(audio_block)
                if result["type"] == "final":
                    print("Final:", result["data"]["text"])
                else:
                    print("Parcial:", result["data"]["partial"])
                    if "menú" in result["data"]["partial"]:
                        self.command_ready.emit()
        except Exception as e:
            print('error:', e)
            pass
        finally:
            self._microphone.close()
            self._voice_detector.finish()

    def stop(self) -> None:
        self._running = False


class MicrophoneThread:
    def __init__(self):
        self._thread: QThread | None  = None
        self._worker: _Worker | None  = None

    def start(self, 
              microphone:   IMicrophoneSource,
              voice_detector: IVoiceDetector, 
              on_command_voice: Callable) -> None:
        
        if self.is_running():
            return

        self._thread = QThread()
        self._worker = _Worker(microphone, voice_detector)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)

        self._worker.command_ready.connect(on_command_voice)
        
        self._thread.start()

    def stop(self) -> None:
        if self._worker:
            self._worker.stop()
        if self._thread:
            self._thread.quit()
            self._thread.wait()

    def is_running(self) -> bool:
        return bool(self._thread and self._thread.isRunning())
