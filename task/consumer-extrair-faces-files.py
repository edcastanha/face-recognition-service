import pika
import json
from datetime import datetime as dt
from lib.deepface import DeepFace
import os
import matplotlib.pyplot as plt
from publicar import Publisher
import re
from loggingMe import logger

import redis

EXCHANGE='secedu'

QUEUE_PUBLISHIR='faces'
ROUTE_KEY='extractor'

QUEUE_CONSUMER='files'
ASK_DEBUG = True


DIR_CAPS ='../volumes/capturas'

#BACKEND_DETECTOR='retinaface'
BACKEND_DETECTOR='Facenet'
MODEL_BACKEND ='mtcnn'
LIMITE_DETECTOR = 0.99

RMQ_SERVER = 'localhost'
REDIS_SERVER = 'localhost'

from os import environ
from redis.commands.search import reducers
from redis.commands.search.query import NumericFilter, Query
import redis.commands.search.aggregation as aggregations

redis_server = environ.get('REDIS_SERVER', "localhost")
logger.info(f' <**_**> redis server definido como ' + redis_server)

redis_port = int(environ.get('REDIS_PORT', "6379"))

server_port = int(environ.get('SERVER_PORT', "8087"))

redis_index = environ.get('REDIS_INDEX', "idx:movies")

redis_password = environ.get('REDIS_PASSWORD', "")

# conn = redis.StrictRedis(redis_server, redis_port)
if redis_password is not None:
    print("REDIS CONNECTION não é None PASSWORD")
    conn = redis.Redis(redis_server, redis_port, password=redis_password, charset="utf-8", decode_responses=True)
else:
    print("SENHA DE LIGAÇÃO AO REDIS")
    conn = redis.Redis(redis_server, redis_port, charset="utf-8", decode_responses=True)

r = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"), decode_responses = True)

#r.delete()
# secedu-rmq-task

class ConsumerExtractor:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RMQ_SERVER,
                port=5672,
                credentials=pika.PlainCredentials('secedu', 'ep4X1!br')
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_bind(
            queue=QUEUE_PUBLISHIR,
            exchange=EXCHANGE,
            routing_key=ROUTE_KEY
        )
        logger.info(f' <**_**> ConsumerExtractor: Init')

    def run(self):
        self.channel.basic_consume(
            queue=QUEUE_CONSUMER,
            on_message_callback=self.process_message,
            auto_ack=ASK_DEBUG
        )

        logger.info(f' <**_**> ConsumerExtractor: Aguardando {QUEUE_CONSUMER}')
        try:
            self.channel.start_consuming()
            logger.info(f' <**_**> ConsumerExtractor: start_consumer')
        finally:
            self.connection.close()
            logger.info(f' <**_**> ConsumerExtractor: close')

    def process_message(self, ch, method, properties, body):
        data = json.loads(body)
        file = data['caminho_do_arquivo']
        logger.info(f' <**_**> ConsumerExtractor: process_message')

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
            face_objs = DeepFace.extract_faces(img_path=file,
                                               detector_backend=BACKEND_DETECTOR, 
                                               enforce_detection=False,  
                                               align=True
                                               )
            # Extrair a parte da URL que contém HH, MM e SS
            matchM = re.search(r'/(\d{2})/(\d{2})/(\d{2})', file)
            if matchM:
                hh, mm, ss = matchM.groups()
                logger.info(f' <**_**> ConsumerExtractor: Math - HH/MM/SS')

            #Extrair a parte da URL que contém HH, MM e SS
            matchP = re.search(r'/(\d{2})/(\d{2})\.(\d{2})', file)
            if matchP:
                hh, mm, ss = matchP.groups()
                logger.info(f' <**_**> ConsumerExtractor: Matc - HH/MM.SS')

            for index, face_obj in enumerate(face_objs):
                if face_obj['confidence'] >= LIMITE_DETECTOR:
                    face = face_obj['face']
                    new_face = os.path.join(DIR_CAPS, equipamento, data_captura, hh,mm,ss)
                    if not os.path.exists(new_face):
                        os.makedirs(new_face, exist_ok=True)

                    # Converta a imagem de float32 para uint8 (formato de imagem)
                    face_uint8 = (face * 255).astype('uint8')
                    
                    # Gere um nome de arquivo único para a face
                    save_path = os.path.join(new_face, f"face_{index}.jpg")
                    logger.info(f' <**_**> ConsumerExtractor: ')
                    
                    try:
                        # Salve a face no diretório "captura/" usando Matplotlib
                        plt.imsave(save_path, face_uint8, format='png', dpi=150)
                        publisher = Publisher()
                        message_dict.update({'caminho_do_face': save_path})
                        message_dict.update({'detector_backend': BACKEND_DETECTOR})
                        message_str = json.dumps(message_dict)
                        publisher.start_publisher(exchange=EXCHANGE, routing_name=ROUTE_KEY, message=message_str)
                        publisher.close()
                        logger.info(f' <**_**> ConsumerExtractor: Save Image')
                    except Exception as e:
                        logger.info(f' <**_**> ConsumerExtractor: {e}')

if __name__ == "__main__":
    job = ConsumerExtractor()
    job.run()