#Navigator class check the stack

class Navigator:
    def __init__(self, main_window):
        self.main_window = main_window
        self.views = {}

    def register(self, name, view):
        self.views[name] = view
        self.main_window.add_view(view)

    def go_to(self, name, h, w):
        view = self.views[name]
        self.main_window.show_view(view, h, w)