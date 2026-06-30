class AppsPresenter():
    def __init__(self, view, navigator, service):
        self.view = view
        self.navigator = navigator
        self.service = service

        self.view.add_apps_clicked.connect(self.on_add_apps_clicked)
        self.view.back_clicked.connect(self.on_back_clicked)
        self.view.open_app_clicked.connect(self.on_open_app_clicked)

    def on_add_apps_clicked(self):
        self.navigator.go_to("appsSelectView", 600, 600)

    def on_back_clicked(self):    
        self.navigator.go_to("homeView", 500, 500)

    def on_open_app_clicked(self, app_path : str, app_title : str, app_icon_path : str):
        print('Open app service')