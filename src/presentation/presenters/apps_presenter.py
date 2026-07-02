from src.domain.models.app_info import AppInfo

class AppsPresenter:
    def __init__(self, view, navigator, config_service, launcher_service):
        self.view = view
        self.navigator = navigator
        self.config_service = config_service
        self.launcher_service = launcher_service
        self.selected_slot = None  # guarda el slot elegido por el usuario

        # Conexiones de señales
        self.view.add_apps_clicked.connect(self.on_add_apps_clicked)          # slots vacíos
        self.view.add_new_app_clicked.connect(self.on_add_new_app_clicked)    # botón superior con slot elegido
        self.view.open_app_clicked.connect(self.on_open_app_clicked)
        self.view.back_clicked.connect(self.on_back_clicked)

        # Cargar rejilla inicial
        self._load_grid()

    def _load_grid(self):
        # Carga los slots desde apps.json
        slots = self.config_service.load_slots()
        self.view.populate_grid(slots)

    def on_add_apps_clicked(self, slot_index: int):
        # Guardamos el slot que el usuario quiere llenar (clic en slot vacío)
        self.selected_slot = slot_index
        self.navigator.go_to("appsSelectView", 600, 600)

    def on_add_new_app_clicked(self, slot_index: int):
        # Guardamos el slot elegido desde la ventana emergente del botón superior
        self.selected_slot = slot_index
        self.navigator.go_to("appsSelectView", 600, 600)

    def on_open_app_clicked(self, app_path: str, app_title: str, app_icon_path: str):
        # Construimos AppInfo y lanzamos la app
        app = AppInfo(name=app_title, exe_path=app_path, icon_path=app_icon_path)
        if not self.launcher_service.launch(app):
            self.view.show_app_not_found(app_title)

    def on_back_clicked(self):
        # Volver a la vista principal
        self.navigator.go_to("homeView", 560, 560)
