class AppsSelectorPresenter():
    def __init__(self, view, navigator, service):
        self.view = view
        self.navigator = navigator
        self.service = service

        self.view.exit_clicked.connect(self.on_exit_clicked)

    def on_exit_clicked(self):    
        self.navigator.go_to("appsView", 500, 800)