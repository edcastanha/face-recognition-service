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
            queue='arquivos',
            on_message_callback=self.process_message,
            auto_ack=True
        )

        print("Esperando por mensagens...")
        try:
            self.channel.start_consuming()
        finally:
            self.connection.close()

    def process_message(self, ch, method, properties, body):
        data = json.loads(body)
        print(data)
        #now = dt.now()
        #proccess = now.strftime("%Y-%m-%d %H:%M:%S")
        #message_dict = {
        #    'data_processo': proccess,
        #    'data_captura': data['data_captura'],
        #    'nome_equipamento': data['nome_equipamento']
        #}

        #detectados = DeepFace.extract_faces()
        

if __name__ == "__main__":
    job = ConsumerExtrair()
    job.run()