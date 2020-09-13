import dlib
import numpy as np
import cv2

class Face_Data:
    def __init__(self, region=(0,0,0,0), landmarks=[0 for i in range(128)]):
        self.region = region
        self.landmarks = landmarks

class Face_Detector:
    def __init__(self):
        self.margin = 10
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('models/face_model.dat')
        self.descript = dlib.face_recognition_model_v1('models/get_descriptors.dat')

    def detect(self, image, margin):
        
        self.margin = margin

        try:
            # detected_faces = self.detector(image, 1)
            detected_faces = self.detector(image, 0)
        except:
            return False, None

        if len(detected_faces) == 0:
            return False, None

        faces_array = []

        for face_count in range(len(detected_faces)):
            region = detected_faces[face_count]

            face_shape = self.predictor(image, region)

            face_descriptor = self.descript.compute_face_descriptor(image, face_shape)
            temp_landmarks = np.array([[p.x, p.y] for p in face_shape.parts()])

            x, y, w, h = cv2.boundingRect(temp_landmarks)

            if not self.margin == 0:
                self.margin = w // 4

            temp_region = (
                            max(x - self.margin, 0),
                            max(y - self.margin, 0),
                            min(x + w  + self.margin, image.shape[1] - 1),
                            min(y + h + self.margin, image.shape[0] - 1)
                        )

            face = Face_Data(region=temp_region, landmarks=temp_landmarks)

            faces_array.append(face)

        return True, faces_array
