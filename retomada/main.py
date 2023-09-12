#QUEUE: arquivos
#ROUTE: path_init
import os 
import pika 
from publicar import Publisher 
import datetime 
import json

PATH_DIR = "ftp/sippe3/Sippe3/" 
RABBITMQ_HOST = "localhost" 
RABBITMQ_QUEUE = "arquivos" 
ROUTE_KEY='path_init'

publicador = Publisher()

def get_file_paths(directory): 
    file_paths = [] 
    for root, directories, files in os.walk(directory): 
        print(f"Files:{root}") 
        for file in files: 
            file_path = os.path.join(root, file) 
            file_paths.append(file_path) 
            #print(file_paths) return file_paths

if __name__ == "main": 
    file_paths = get_file_paths(PATH_DIR)

    for file_path in file_paths:
        now = datetime.datetime.now()
        dia_atual = now.strftime("%Y-%m-%d")
        hora_atual = now.strftime("%H:%M:%S")

        # Cria um dicionário
        message_dict = {
            "file_path": file_path,
            "dia": dia_atual, 
            "hora": hora_atual,
            "local_id" : 3
            }

        # Serializa o dicionário em uma string JSON
        message_str = json.dumps(message_dict)

        publicador.call(message_str, routing_name='path_init')

        publicador.close()