from abc import ABC, abstractmethod

class IMouseController(ABC):
    """
        Interface for the mouse controller
    """
    
    @abstractmethod
    def move_to(self, x, y):
        """
        Move the cursor to a screen position specified by x and y coordinates.

        Args:
            x: x-coordinate
            y: y-coordinate
        """
        ...
    
    
    @abstractmethod
    def click_at(self, x, y):
        """
        Click on point x and enter the following parameters
        
        Args:
            x: x-coordinate
            y: y-coordinate
        """
        ...