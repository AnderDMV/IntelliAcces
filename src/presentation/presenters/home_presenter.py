class HomePresenter():
    def __init__(self, view, navigator, service):
        self.view = view
        self.navigator = navigator
        self.service = service

        self.view.calibration_clicked.connect(self.on_calibration_clicked)
        self.view.camera_state_clicked.connect(self.on_state_clicked)
        self.view.apps_clicked.connect(self.on_apps_clicked)

    def on_calibration_clicked(self):
        self.navigator.go_to("calibrationView", 800, 800)

    def on_apps_clicked(self):    
        self.navigator.go_to("appsView", 500, 800)


    def on_state_clicked(self):
        self.navigator.go_to("cameraStateView", 800, 800)
