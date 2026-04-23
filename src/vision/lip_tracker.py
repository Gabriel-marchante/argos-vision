import cv2
import face_recognition

class LipTracker:
    def __init__(self):
        pass

    def get_lip_landmarks(self, frame):
        """Extract lip landmarks from the frame."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        landmarks_list = face_recognition.face_landmarks(rgb_frame)
        
        if not landmarks_list:
            return None
            
        # Get first face
        face_landmarks = landmarks_list[0]
        
        lips = []
        if 'top_lip' in face_landmarks:
            lips.extend(face_landmarks['top_lip'])
        if 'bottom_lip' in face_landmarks:
            lips.extend(face_landmarks['bottom_lip'])
            
        return lips if lips else None

    def draw_lips(self, frame, lips):
        """Highlight lips on the frame."""
        if lips:
            for pt in lips:
                cv2.circle(frame, pt, 1, (0, 0, 255), -1)

