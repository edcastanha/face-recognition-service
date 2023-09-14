import pika
import json
from datetime import datetime as dt
import re
import os

from publicar import Publisher

class Consumer:
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
            queue='arquivos',
            exchange='secedu',
            routing_key='path_init'
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
                    message_dict.update({'caminho_do_arquivo': file_path})
                    
                    message_str = json.dumps(message_dict)
                    publisher.start_publisher(message=message_str, routing_name='extrair-face')
                publisher.close()


    def find_image_files(self, path):
        file_paths = []
        for root, directories, files in os.walk(path):
            for file in files:
                if file.lower().endswith(('[0].jpg', '[0].jpeg', '[0].png')):
                    file_path = os.path.join(root, file)
                    file_paths.append(file_path)
        return file_paths

if __name__ == "__main__":
    job = Consumer()
    job.run()