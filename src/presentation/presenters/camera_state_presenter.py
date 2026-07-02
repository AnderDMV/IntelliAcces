class CameraStatePresenter():
    def __init__(self, view, navigator):
        self.view = view
        self.navigator = navigator

        self.view.back_clicked.connect(self.on_back_clicked)
        
    def on_back_clicked(self):    
        self.navigator.go_to("homeView", 560, 560)