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
        self.publisher = Publisher()
        self.channel = self.connection.channel()
        self.channel.queue_bind(
            exchange='secedu',
            queue='arquivos',
            routing_key='path_init'
        )
    
    @staticmethod
    def get_folders_with_date_format(directory):
        folder_paths = []
        
        for root, directories, files in os.walk(directory):
            for directory in directories:
                # Verifica se o nome da pasta corresponde ao formato AAAA-MM-DD
                if re.match(r"\d{4}-\d{2}-\d{2}$", directory):
                    folder_path = os.path.join(root, directory)
                    folder_paths.append(folder_path)

            return folder_paths

    def start_consumer(self):
        self.channel.basic_consume(
            queue='arquivos',
            on_message_callback=self.callback,
            auto_ack=False
        )

        print("Esperando por mensagens...")
        try:
            print('Start Consumer')
            self.channel.start_consuming()
        finally:
            print('Close Consumer')
            self.connection.close()

    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        for index, field_name in data.items():
            now = dt.now()
            proccess = now.strftime("%Y-%m-%d %H:%M:%S")
            message_dict = {
                "proccess": proccess,
            }
            if index == 'file_path':
                file_paths = []
                for root, directories, files in os.walk(field_name):
                    for file in files:
                        # Verifica se o arquivo tem uma extensão de imagem válida
                        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                            file_path = os.path.join(root, file)
                            message_dict.update({'path_image': file_path})
                            
                        #print(message_dict)
                        message_str = json.dumps(message_dict)
                        self.publisher.start_publisher(self.rabbitmq_queue, message_str, self.route_key)
            self.publisher.close()
    
    

if __name__ == "__main__":
    job = Consumer()
    job.start_consumer()
