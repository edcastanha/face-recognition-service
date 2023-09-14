import pika
import json
from datetime import datetime as dt
from deepface import DeepFace
import os
import matplotlib.pyplot as plt
from publicar import Publisher
import logging
import numpy as np

DIR_CAPS ='../capturas/'
backend_detector='retinaface'

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
        logging.info('Started Class...')

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
        file = data['caminho_do_arquivo']
        print(file)

        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            now = dt.now()
            equipamento =data['nome_equipamento']
            data_captura=data['data_captura']
            proccess = now.strftime("%Y-%m-%d %H:%M:%S")
            message_dict = {
                'data_processo': proccess,
                'data_captura': data_captura,
                'nome_equipamento': equipamento,
                'captura_base': file,
            }
            face_objs = DeepFace.extract_faces(img_path=file, detector_backend=backend_detector, enforce_detection=False)
            for index, face_obj in enumerate(face_objs):
                if face_obj['confidence'] >= 0.97:
                    face = face_obj['face']
                    # Verifique se pelo menos um rosto atende ao critério de confiança
                    new_face = os.path.join(DIR_CAPS, equipamento, data_captura)
                    if not os.path.exists(new_face):
                        os.makedirs(new_face, exist_ok=True)
                    # Converta a imagem de float32 para uint8 (formato de imagem)
                    face_uint8 = (face * 255).astype('uint8')
                    
                    # Gere um nome de arquivo único para a face
                    save_path = os.path.join(new_face, f"face_{index}.jpg")

                    try:
                        # Salve a face no diretório "captura/" usando Matplotlib
                        plt.imsave(save_path, face_uint8)
                        
                        publisher = Publisher()
                        message_dict.update({'caminho_do_face': save_path})
                        message_dict.update({'detector_backend': backend_detector})

                        message_str = json.dumps(message_dict)
                        #publisher.start_publisher(message=message_str, routing_name='embedding')
                        publisher.close()
                        
                        print("Face saved:", save_path)
                    except Exception as e:
                        print("Erro ao salvar a imagem:", str(e))

if __name__ == "__main__":
    job = ConsumerExtrair()
    job.run()