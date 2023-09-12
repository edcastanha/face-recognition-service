rom deepface import DeepFace
from PIL import Image

class FaceDetector:
    def __init__(self, path_image, camera_id):
        self.path_image = path_image
        self.camera_id = camera_id
        
        #DeepFace.build_model('DeepFace')
    def start_detection(self):
        detections = DeepFace.extract_faces(
        img_path=self.path_image,
        target_size=(224, 224),
        detector_backend='retinaface',
        enforce_detection=False,
        align=True
        )
        for i, face_data in enumerate(detections):
            print(f"ID-{i}: {face_data['face']}")
            face_image = Image.fromarray(face_data['image'])
            confidence = face_data['confidence']
            facial_area = face_data['facial_area']
            x1, y1, x2, y2 = facial_area[0], facial_area[1], facial_area[2], facial_area[3]
            roi = face_image.crop((x1, y1, x2, y2))
            # Salvar a imagem em um arquivo JPG
            file_name = f"face_{i}.jpg"
            roi.save(file_name)
            # Resto do código...

if __name__ == '__main__':
    path_img = 'ftp/sippe3/Sippe3/2023-08-03/001/jpg/08/25.03[M][0@0][0].jpg'
    job = FaceDetector(path_img, 'Device 1')
    job.start_detection()