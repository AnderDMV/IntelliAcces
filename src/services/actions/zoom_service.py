from src.domain.interfaces.i_zoom_screen import IZoomScreen
import win_magnification as mag

class ZoomService(IZoomScreen):
    def __init__(self):
        self.run = False
        self.size_screen = (1920, 1080)
        self.zoom_times = 1.0
    
    #Override
    def zoom_in_coords(self, x_cord : int, y_cord : int):
        if self.zoom_times < 4:
            zoom_porcent = self.zoom_times + 1.0
            mag.set_fullscreen_transform(zoom_porcent, (x_cord - self._cords_reduction(zoom_porcent)['x'], y_cord - self._cords_reduction(zoom_porcent)['y']))

    #Override
    def zoom_revert(self):
        self.zoom_times = 1.0
        mag.reset_fullscreen_transform()

    def start(self):
        if self.run:
            mag.initialize()
    
    def _cords_reduction(self, zoom_porcent):
        x_reduction = self.size_screen[0] / (zoom_porcent * 2)
        y_reduction = self.size_screen[1] / (zoom_porcent * 2)
        return {'x': x_reduction, 'y' : y_reduction}
    
    