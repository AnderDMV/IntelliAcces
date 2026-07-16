import sounddevice as sd
import queue

class MicrophoneService:
    """
    Sirve para capturar y reproducir audio usando la API de portaudio, interactua con hardware y maneja su propio bucle interno que ejecuta callback constantemente al
    captar una nueva pista, callback() guarda la pista en una Queue o cola la cual posteriormente será usada por el detector de voz
    Se pasara antes dicha pista como PCM (int16, mono, frecuencia definida en vosk)
    """
    
    def __init__(self, samplerate : int = 16000, blocksize : int = 8000 ):
        self.audio_queue = queue.Queue()
        self.samplerate = samplerate
        self.blocksize = blocksize
        
        self.stream = sd.RawInputStream(
            samplerate=samplerate,
            blocksize=blocksize,
            dtype='int16',
            channels=1,
            callback= self._callback)
        
        
    def _callback(self, indata, frames, time, status):
        self.audio_queue.put(bytes(indata))
    
    def start(self):
        self.stream.start()

    
    def read_audio(self):
        return self.audio_queue.get()
    
    
    def close(self):
        self.stream.stop()
        self.stream.close()