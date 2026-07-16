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
        Procesa un bloque de audio en bytes PCM.
        Devuelve un dict con resultado parcial o final.
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
