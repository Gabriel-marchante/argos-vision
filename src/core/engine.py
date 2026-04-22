import cv2
import time
import threading
from src.vision.face_detector import FaceDetector
from src.vision.lip_tracker import LipTracker
from src.audio.recorder import AudioRecorder
from src.audio.transcriber import Transcriber
from src.ai.profiler import Profiler
from src.database.db_manager import DBManager

class ArgosEngine:
    def __init__(self, ai_provider="openai"):
        self.db = DBManager()
        self.vision = FaceDetector()
        self.lip_tracker = LipTracker()
        self.recorder = AudioRecorder()
        self.transcriber = Transcriber()
        self.profiler = Profiler(provider=ai_provider)
        
        self.running = False
        self.current_person_id = None
        self.last_detection_time = 0
        self.unknown_counter = 0

    def start(self):
        self.running = True
        # Start camera thread
        video_thread = threading.Thread(target=self._video_loop)
        video_thread.start()
        
        # Start audio analysis loop
        audio_thread = threading.Thread(target=self._audio_loop)
        audio_thread.start()

    def _video_loop(self):
        cap = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detect faces
            face_locations, face_names = self.vision.detect_and_recognize(frame)
            
            # Tracking lips
            lip_pts = self.lip_tracker.get_lip_landmarks(frame)
            self.lip_tracker.draw_lips(frame, lip_pts)

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Update current person tracking
                person = None
                if name == "Unknown":
                    # Check if we should register new person
                    # For now, let's just use a temporary alias
                    alias = f"sinreconocer_{self.unknown_counter}"
                    # Check if we already have this "Unknown" in this session or DB
                    person = self.db.get_or_create_person(alias=alias)
                    # Train vision on it
                    face_img = self.vision.get_face_image(frame, (top, right, bottom, left))
                    self.vision.add_new_face(face_img, alias)
                    self.unknown_counter += 1
                    name = alias
                else:
                    person = self.db.get_or_create_person(full_name=name)
                
                if person:
                    self.current_person_id = person.id
                    self.last_detection_time = time.time()
                    self.db.add_detection(person.id, 0.9) # TODO: actual confidence

                # Draw overlay
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            cv2.imshow('ARGOS Panoptes', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break
        
        cap.release()
        cv2.destroyAllWindows()

    def _audio_loop(self):
        while self.running:
            # Only record if someone is being detected (to save resources)
            if time.time() - self.last_detection_time < 5.0 and self.current_person_id:
                chunk_path = self.recorder.record_chunk(seconds=5, filename=f"chunk_{int(time.time())}.wav")
                transcript = self.transcriber.transcribe(str(chunk_path))
                
                if transcript and self.current_person_id:
                    print(f"Transcript: {transcript}")
                    self.db.add_transcript(self.current_person_id, transcript)
                    
                    # AI Enrichment
                    person_id = self.current_person_id
                    # Get existing profiles to enrich
                    # TODO: Fetch existing profiles from DB and pass to profiler
                    info = self.profiler.extract_information(transcript)
                    print(f"AI Extracted Info: {info}")
                    
                    # Save to DB
                    for category, content in info.items():
                        self.db.update_profile(person_id, category, str(content))
            else:
                time.sleep(1)

    def stop(self):
        self.running = False
