import pyaudio
import wave
import os
import threading
from pathlib import Path

class AudioRecorder:
    def __init__(self, output_dir="data/audio_chunks"):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000 # Whisper likes 16kHz
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.recording = False
        self.thread = None

    def start_recording(self):
        self.frames = []
        self.recording = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()
        print("Recording started...")

    def _record(self):
        stream = self.p.open(format=self.format,
                            channels=self.channels,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=self.chunk)
        while self.recording:
            data = stream.read(self.chunk)
            self.frames.append(data)
        
        stream.stop_stream()
        stream.close()

    def stop_recording(self, filename="temp.wav"):
        self.recording = False
        if self.thread:
            self.thread.join()
        
        output_path = self.output_dir / filename
        wf = wave.open(str(output_path), 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print(f"Recording saved to {output_path}")
        return output_path

    def __del__(self):
        self.p.terminate()
        
    def record_chunk(self, seconds=5, filename="chunk.wav"):
        """Sync recording for a fixed duration."""
        stream = self.p.open(format=self.format,
                            channels=self.channels,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=self.chunk)
        
        print(f"Recording {seconds} seconds...")
        frames = []
        for _ in range(0, int(self.rate / self.chunk * seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
            
        stream.stop_stream()
        stream.close()
        
        output_path = self.output_dir / filename
        wf = wave.open(str(output_path), 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        return output_path
