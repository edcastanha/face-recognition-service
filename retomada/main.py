import os
import re
import json
from datetime import datetime
import logging

from publicar import Publisher

# Path padrao 
ftp_folder = '../ftp'

# Expressão regular para o padrão AAAA-MM-DD
date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

# Percorrer a pasta FTP
for root, dirs, files in os.walk(ftp_folder):
    for dir in dirs:
        # Verificar se a subpasta corresponde ao padrão AAAA-MM-DD
        if date_pattern.match(dir):
            print(f'Inicial...')
            components = root.split('/')
            device_name = components[2]
            date_capture = dir
            timestamp = datetime.now().isoformat()
            file_path = os.path.join(root, dir)
            #print(file_path)
            message_dict = {
                "data_processomento": timestamp,
                "caminho_do_arquivo": file_path,
                "data_captura": date_capture,
                "nome_equipamento": device_name
            }

            message_str = json.dumps(message_dict)

            print(f'Message: {message_str}')
            try:
                logging.info('Publisher Main')

                publisher = Publisher()

                publisher.start_publisher(
                    message=message_str, 
                    routing_name='path_init'
                    )
                publisher.close()
            except pika.exceptions.AMQPConnectionError as e:
                logging.info(f'Exceptions Main: {e}')
                print(f"Erro ao estabelecer conexão com o RabbitMQ: {e}")
            
    

