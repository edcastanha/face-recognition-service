import pika
import json
from datetime import datetime as dt
import re
import os
import logging

from publicar import Publisher

class ConsumerExtratorFace:
    logging.info(f'CLASS: <#:#> ConsumerExtratorFace')

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
            exchange='secedu',
            queue='extrair',
            routing_key='extrair-face'
        )

    def run(self):
        self.channel.basic_consume(
            queue='extrair',
            on_message_callback=self.process_message,
            #auto_ack=True
        )

        print("Esperando por mensagens...")
        try:
            self.channel.start_consuming()
        finally:
            self.connection.close()

    def process_message(self, ch, method, properties, body):
        data = json.loads(body)
        for index, field_name in data.items():
            now = dt.now()
            proccess = now.strftime("%Y-%m-%d %H:%M:%S")
            message_dict = {
                "proccess": proccess,
            }
            if index == 'file_path':
                file_paths = self.find_image_files(field_name)
                publisher = Publisher()
                for file_path in file_paths:
                    message_dict.update({'path_image': file_path})
                    message_str = json.dumps(message_dict)
                    print(message_str)
                    publisher.start_publisher(message=message_str, routing_name='busca-imagem')
                publisher.close()

    def find_image_files(self, path):
        file_paths = []
        for root, directories, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    file_path = os.path.join(root, file)
                    file_paths.append(file_path)
        return file_paths


if __name__ == "__main__":
    job = Consumer()
    job.run()