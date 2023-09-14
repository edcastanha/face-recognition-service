import pika
import json
from datetime import datetime as dt
from deepface import DeepFace
import os

from publicar import Publisher

class ConsumerExtrair:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                credentials=pika.PlainCredentials('secedu', 'ep4X1!br')
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_bind(
            queue='extrair',
            exchange='secedu',
            routing_key='extrair-face'
        )

    def run(self):
        # CONFIGURACAO CONSUMER
        self.channel.basic_consume(
            queue='extrair',
            on_message_callback=self.process_message,
            auto_ack=False
        )

        print("Esperando por mensagens...")
        try:
            self.channel.start_consuming()
        finally:
            self.connection.close()

    def process_message(self, ch, method, properties, body):
        data = json.loads(body)
        model_names = [
            "VGG-Face",
            "Facenet",
            "Facenet512",
            "OpenFace",
            "DeepFace",
            "DeepID",
            "Dlib",
            "ArcFace",
            "SFace",
        ]
        detector_backends = ["opencv", "ssd", "dlib", "mtcnn", "retinaface"]

        now = dt.now()
        proccess = now.strftime("%Y-%m-%d %H:%M:%S")
        message_dict = {
            'data_processo': proccess,
            'data_captura': data['data_captura'],
            'nome_equipamento': data['nome_equipamento']
        }
        for index, field_name in data.items():
                    
            if index == 'caminho_do_arquivo':
                file_paths = self.find_image_files(field_name)
                publisher = Publisher()
                for file_path in file_paths:
                    # extract faces
                    for detector_backend in detector_backends:
                        face_objs = DeepFace.extract_faces(
                            img_path="dataset/img1.jpg", detector_backend=detector_backend
                        )
                        for face_obj in face_objs:
                            face = face_obj["face"]
                            print(detector_backend)
                            # represent
                            for model_name in model_names:
                                embedding_objs = DeepFace.represent(img_path=face, model_name=model_name)
                                for embedding_obj in embedding_objs:
                                    embedding = embedding_obj["embedding"]
                                    print(f"{model_name} produced {len(embedding)}D vector")

    def find_image_files(self, path):
        file_paths = []
        for root, directories, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('[0].jpg', '[0].jpeg', '[0].png')):
                    file_path = os.path.join(root, file)
                    file_paths.append(file_path)
        return file_paths
if __name__ == "__main__":
    job = ConsumerExtrair()
    job.run()