from abc import ABC, abstractmethod

class IMicrophoneSource(ABC):
    
    @abstractmethod
    def start():
        ...
        
    @abstractmethod        
    def read_audio():
        ...
        
    @abstractmethod        
    def close():
        ...