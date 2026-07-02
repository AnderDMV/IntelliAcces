from src.domain.models.app_info import AppInfo

class AppsSelectorPresenter:
    def __init__(self, view, navigator, installed_service, config_service, apps_presenter):
        self.view = view
        self.navigator = navigator
        self.installed_service = installed_service
        self.config_service = config_service
        self.apps_presenter = apps_presenter  # referencia al presenter de la rejilla

        # Conexiones de señales
        self.view.exit_clicked.connect(self.on_exit_clicked)
        self.view.app_selected.connect(self.on_app_selected)

        # Cargar apps disponibles
        self._load_apps()

    def _load_apps(self):
        # Obtiene apps reales desde InstalledAppsService
        apps = self.installed_service.get_apps()
        self.view.load_apps(apps)

    def on_exit_clicked(self):
        # Volver a la rejilla sin asignar nada
        self.navigator.go_to("appsView", 500, 800)

    def on_app_selected(self, app: AppInfo):
        slot = self.apps_presenter.selected_slot
        if slot is not None:
            self.config_service.assign_app(slot, app)
            # Refrescar la rejilla inmediatamente
            self.apps_presenter._load_grid()
        # Volvemos a la rejilla para mostrar la app en su posición
        self.navigator.go_to("appsView", 500, 800)
