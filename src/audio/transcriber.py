import whisper
import os
from pathlib import Path

class Transcriber:
    def __init__(self, model_name="base"):
        print(f"Loading Whisper model: {model_name}...")
        self.model = whisper.load_model(model_name)
        print("Whisper model loaded.")

    def transcribe(self, audio_path):
        """Transcribe an audio file to text."""
        if not os.path.exists(audio_path):
            return ""
        
        result = self.model.transcribe(audio_path)
        return result["text"].strip()
