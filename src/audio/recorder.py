import sounddevice as sd
import numpy as np
import wave
import os
import threading
from pathlib import Path

class AudioRecorder:
    def __init__(self, output_dir="data/audio_chunks"):
        self.channels = 1
        self.rate = 16000 # Whisper likes 16kHz
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.frames = []
        self.recording = False
        self.thread = None
        self.stream = None

    def start_recording(self):
        self.frames = []
        self.recording = True
        
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.frames.append(indata.copy())
            
        self.stream = sd.InputStream(samplerate=self.rate, channels=self.channels, dtype='int16', callback=callback)
        self.stream.start()
        print("Recording started...")

    def stop_recording(self, filename="temp.wav"):
        self.recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            
        output_path = self.output_dir / filename
        if self.frames:
            audio_data = np.concatenate(self.frames, axis=0)
            with wave.open(str(output_path), 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2) # 2 bytes for int16
                wf.setframerate(self.rate)
                wf.writeframes(audio_data.tobytes())
        print(f"Recording saved to {output_path}")
        return output_path

    def __del__(self):
        if hasattr(self, 'stream') and self.stream is not None:
            self.stream.close()
        
    def record_chunk(self, seconds=5, filename="chunk.wav"):
        """Sync recording for a fixed duration."""
        print(f"Recording {seconds} seconds...")
        audio_data = sd.rec(int(seconds * self.rate), samplerate=self.rate, channels=self.channels, dtype='int16')
        sd.wait() # Wait until recording is finished
        
        output_path = self.output_dir / filename
        with wave.open(str(output_path), 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2) # 2 bytes for int16
            wf.setframerate(self.rate)
            wf.writeframes(audio_data.tobytes())
        return output_path
