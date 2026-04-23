import cv2
import face_recognition
import numpy as np
import os
from pathlib import Path

class FaceDetector:
    def __init__(self, known_faces_dir="data/known_faces"):
        self.known_faces_dir = Path(known_faces_dir)
        self.known_faces_dir.mkdir(parents=True, exist_ok=True)
        
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    def load_known_faces(self):
        """Load all face images from the known_faces directory and encode them."""
        for img_path in self.known_faces_dir.glob("*.jpg"):
            name = img_path.stem
            image = face_recognition.load_image_file(str(img_path))
            encodings = face_recognition.face_encodings(image)
            if encodings:
                self.known_face_encodings.append(encodings[0])
                self.known_face_names.append(name)
        print(f"Loaded {len(self.known_face_names)} known faces.")

    def add_new_face(self, image, name):
        """Save a new face image and its encoding."""
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb_image)
        if encodings:
            img_path = self.known_faces_dir / f"{name}.jpg"
            cv2.imwrite(str(img_path), image)
            self.known_face_encodings.append(encodings[0])
            self.known_face_names.append(name)
            return True
        return False

    def detect_and_recognize(self, frame):
        """Detect faces in a frame and attempt to recognize them."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces using face_recognition
        face_locations = face_recognition.face_locations(rgb_frame)
        
        # Encode detected faces
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        face_names = []
        for face_encoding in face_encodings:
            # Check for matches
            name = "Unknown"
            if self.known_face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.6)
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
            
            face_names.append(name)
            
        return face_locations, face_names

    def get_face_image(self, frame, location):
        """Extract a face image from the frame given its location."""
        top, right, bottom, left = location
        return frame[top:bottom, left:right]
