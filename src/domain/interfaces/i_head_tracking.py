from abc import ABC, abstractmethod

class IHeadTracking(ABC):
    
    @abstractmethod
    def get_position():
        ...