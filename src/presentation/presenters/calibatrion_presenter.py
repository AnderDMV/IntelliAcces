class CalibrationPresenter():
    def __init__(self, view, navigator):
        self.view = view
        self.navigator = navigator

        self.view.confirm_clicked.connect(self.on_confirm_clicked)
        
    def on_confirm_clicked(self):    
        self.navigator.go_to("homeView", 560, 560)