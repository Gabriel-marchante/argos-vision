import cv2
import mediapipe as mp

class LipTracker:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Landmark indices for lips (simplified)
        self.LIP_OUTER = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291]
        self.LIP_INNER = [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308]

    def get_lip_landmarks(self, frame):
        """Extract lip landmarks from the frame."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if not results.multi_face_landmarks:
            return None
            
        face_landmarks = results.multi_face_landmarks[0]
        h, w, _ = frame.shape
        
        lips = []
        for idx in self.LIP_OUTER + self.LIP_INNER:
            landmark = face_landmarks.landmark[idx]
            lips.append((int(landmark.x * w), int(landmark.y * h)))
            
        return lips

    def draw_lips(self, frame, lips):
        """Highlight lips on the frame."""
        if lips:
            for pt in lips:
                cv2.circle(frame, pt, 1, (0, 0, 255), -1)
