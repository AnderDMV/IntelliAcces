import sounddevice as sd
import queue

class MicrophoneService:
    """
    Captures microphone audio using the PortAudio API.
    Continuously captures audio and stores it in a queue within its own thread.
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
        """Constantly saves data tracks to the queue"""
        self.audio_queue.put(bytes(indata))
    
    def start(self):
        """Constantly saves data tracks to the queue"""
        self.stream.start()

    
    def read_audio(self):
        return self.audio_queue.get()
    
    
    def close(self):
        self.stream.stop()
        self.stream.close()