import vosk
import json

class VoiceDetector:
    
    def __init__(self, model_path="src/services/mic/vosk-model-small-es-0.42", samplerate=16000):
        # Cargar modelo de Vosk
        
        self.model = vosk.Model(model_path)
        # Crear reconocedor
        self.recognizer = vosk.KaldiRecognizer(self.model, samplerate)

    def process(self, audio_bytes):
        """
        Processes the audio block audio in bytes PCM.
        Returns dict with the final or partial result.
        """
        if self.recognizer.AcceptWaveform(audio_bytes):
            return {"type": "final", "data": json.loads(self.recognizer.Result())}
        else:
            return {"type": "partial", "data": json.loads(self.recognizer.PartialResult())}
        
    def stream_process(self, audio_bytes):
        pass
        
    def phrase_process(self, audio_bytes):
        if self.recognizer.AcceptWaveform(audio_bytes):
            return {"type": "final", "data": json.loads(self.recognizer.Result())}    

    def finish(self):
        """
        Devuelve el resultado final acumulado al terminar la captura.
        """
        return json.loads(self.recognizer.FinalResult())
