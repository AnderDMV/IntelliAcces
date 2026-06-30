from abc import ABC, abstractmethod

class ICameraSource(ABC):
    
    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def get_frame(self):
        ...

    @abstractmethod
    def is_active(self) -> bool:
        ...
