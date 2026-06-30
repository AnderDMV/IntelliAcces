class HomePresenter():
    def __init__(self, view, navigator, service):
        self.view = view
        self.navigator = navigator
        self.service = service

        self.view.microphone_clicked.connect(self.on_microphone_clicked)
        self.view.extra_clicked.connect(self.on_extra_clicked)
        self.view.apps_clicked.connect(self.on_apps_clicked)

    def on_microphone_clicked(self):
        self.navigator.go_to("calibrationView", 800, 800)

    def on_apps_clicked(self):    
        self.navigator.go_to("appsView", 500, 800)


    def on_extra_clicked(self):
        self.navigator.go_to("cameraStateView", 800, 800)
