from src.infrastructure.threads.camera_thread import CameraThread
from src.infrastructure.threads.microphone_thread import MicrophoneThread

from src.presentation.main_window import MainWindow
from src.presentation.overlay_window import OverlayWindow
from src.presentation.navigator import Navigator

from src.presentation.views.home_view import HomeView
from src.presentation.views.calibration_view import CalibrationView 
from src.presentation.views.camera_state_view import CameraStateView
from src.presentation.views.apps_view import AppsView
from src.presentation.views.apps_selector_view import AppsSelectorView

from src.presentation.presenters.overlay_presenter import OverlayPresenter
from src.presentation.presenters.calibatrion_presenter import CalibrationPresenter
from src.presentation.presenters.camera_state_presenter import CameraStatePresenter
from src.presentation.presenters.home_presenter import HomePresenter
from src.presentation.presenters.apps_presenter import AppsPresenter 
from src.presentation.presenters.apps_selector_presenter import AppsSelectorPresenter

from src.services.mic.microphone_service import MicrophoneService
from src.services.mic.voice_detector import VoiceDetector

from src.services.vision.camera_service import CameraService
from src.services.vision.head_tracking_service import HeadTrackingService
from src.services.vision.blink_gesture_detector import BlinkGestureDetector
from src.services.vision.brow_gesture_detector import BrowGestureDetector
from src.services.vision.face_pipeline import FacePipeline
from src.services.main_service import MainService
from src.services.apps.apps_config_service import AppsConfigService
from src.services.apps.apps_launcher_service import AppLauncherService
from src.services.apps.installed_apps_service import InstalledAppsService

class Application():
    #Dependencies
    def __init__(self, qt_app):
        self._qt_app = qt_app
        self._build()
        
    def _build(self):
        #Threads
        self._camera_threads = CameraThread()
        self._microphone_thread = MicrophoneThread()

        #Windows
        self._overlay_window = OverlayWindow()#Overlay Window - draw circle
        self._mainWindow = MainWindow()#Main Window visual - with stacks

        #Navigator (control the stack)
        navigator = Navigator(self._mainWindow)
        
        #Services
        self._camera_service = CameraService()
        self._microphone_service = MicrophoneService()
        self._voice_detector = VoiceDetector()
        self._mainService = MainService()
        self._apps_config_service = AppsConfigService()
        self._apps_launcher_service = AppLauncherService()
        self._installed_apps_service = InstalledAppsService()
        self._blink_gesture_detector = BlinkGestureDetector()
        self._brow_gesture_detector = BrowGestureDetector()
        self._head_tracking_service = HeadTrackingService()
        self._face_pipeline = FacePipeline(self._head_tracking_service, self._blink_gesture_detector, self._brow_gesture_detector)
        
        #Views
        self._home_view = HomeView()
        self._calibration_view = CalibrationView()
        self._camera_state_view = CameraStateView()
        self._apps_view = AppsView()
        self._apps_select_view = AppsSelectorView()

        #Presenters
        self._overlay_presenter = OverlayPresenter(self._overlay_window,
                                                   navigator, 
                                                   self._calibration_view, 
                                                   self._camera_state_view, 
                                                   self._camera_threads, 
                                                   self._microphone_thread, 
                                                   self._microphone_service,
                                                   self._voice_detector, 
                                                   self._camera_service, 
                                                   self._face_pipeline)
        self._camera_state_presenter = CameraStatePresenter(self._camera_state_view, navigator)
        self._calibration_presenter = CalibrationPresenter(self._calibration_view, navigator)
        self._home_presenter = HomePresenter(self._home_view, navigator , self._mainService)
        self._apps_presenter = AppsPresenter(self._apps_view, navigator, self._apps_config_service, self._apps_launcher_service)
        self._apps_select_presenter = AppsSelectorPresenter(self._apps_select_view, navigator, self._installed_apps_service, self._apps_config_service, self._apps_presenter)

        #Register navigators
        navigator.register("calibrationView", self._calibration_view)
        navigator.register("homeView",self._home_view)
        navigator.register("cameraStateView", self._camera_state_view)
        navigator.register("appsView",self._apps_view)
        navigator.register("appsSelectView", self._apps_select_view)
        

    def start(self):
        self._mainWindow.show()
        self._overlay_window.show()