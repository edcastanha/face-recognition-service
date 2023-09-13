import os
import pika
import datetime
import json
import re
from publicar import Publisher
from deep

class Detection():
    def __init__(self):
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=pika.PlainCredentials('sippe', 'ep4X1!br')))
            self.channel = self.connection.channel()
        
    def start_task(self):
        file_paths = self.get_folders_with_date_format(self.path_dir)
        for file_path in file_paths:
            now = datetime.datetime.now()
            proccess = now.strftime("%Y-%m-%d %H:%M:%S")
            message_dict = {
                "file_path": file_path,
                "proccess": proccess,
                "local_id" : 'sippe3',
                "dia": self.dia_captura,
                "hora": self.hora_captura
            }
        message_str = json.dumps(message_dict)
        self.publisher.start_publisher(self.rabbitmq_queue, message_str, self.route_key)
        self.publisher.close()

    def get_folders_with_date_format(self, directory):
        folder_paths = []
        for root, directories, files in os.walk(directory):
            for directory in directories:
                # Verifica se o nome da pasta corresponde ao formato AAAA-MM-DD
                if re.match(r"\d{4}-\d{2}-\d{2}$", directory):
                    folder_path = os.path.join(root, directory)
                    folder_paths.append(folder_path)
                    # Extrair a data
                    matchDia = re.search(r'(\d{4}-\d{2}-\d{2})', directory)
                    if matchDia:
                        self.dia_captura = matchDia.group(1)
                        # Extrair a hora
                        matchHora = re.search(r'\d{4}-\d{2}-\d{2}/\d{3}/jpg/(\d{2})/(\d{2})\.(\d{2})', 
                        directory)
                    if matchHora:
                        self.hora_captura = f"{matchHora.group(1)}:{matchHora.group(2)}:
                        {matchHora.group(3)}"

            return folder_paths


if __name__ == "__main__":
    PATH_DIR = "ftp/sippe3/Sippe3/"
    RABBITMQ_QUEUE = "arquivos"
    ROUTE_KEY = 'path_init'
    job = Detection()
