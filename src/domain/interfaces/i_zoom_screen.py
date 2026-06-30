from abc import ABC, abstractmethod

class IZoomScreen(ABC):
    @abstractmethod
    def zoom_in_coords(self, x_cord : int, y_cord : int):
        ...
    
    @abstractmethod
    def zoom_revert(self):
        ...