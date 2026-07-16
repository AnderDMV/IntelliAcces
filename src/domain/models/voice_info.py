from dataclasses import dataclass


@dataclass(slots=True)
class VoiceInfo:
    type: str
    text: str