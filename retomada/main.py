import os
import re
import json
from datetime import datetime
import pika
from loggingMe import logger

from publicar import Publisher

logger.info(f' <**_**> Main - Processando pasta do FTP')

#QUEUE_PUBLISHIR='ftp'
#QUEUE_CONSUMER='arquivos'
EXCHANGE='secedu'
ROUTE_KEY='path'
FTP_PATH = '../ftp'

# Expressão regular para o padrão AAAA-MM-DD
date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

# Percorrer a pasta FTP
for root, dirs, files in os.walk(FTP_PATH):
    logger.info(f' <**_**> Iniciado listagem de PATH DEVICE')
    for dir in dirs:
        logger.info(f' <**_**> PATH: {dir}')
        # Verificar se a subpasta corresponde ao padrão AAAA-MM-DD
        if date_pattern.match(dir):
            components = root.split('/')
            device_name = components[2]
            date_capture = dir
            timestamp = datetime.now().isoformat()
            file_path = os.path.join(root, dir)
            logger.info(f' <**_**> PATH: {file_path}')
            message_dict = {
                "data_captura": date_capture,
                "nome_equipamento": device_name,
                "caminho_do_arquivo": file_path,
                "data_processomento": timestamp,
            }

            message_str = json.dumps(message_dict)

            print(f'{message_str}')
            try:
                logger.info(f' <**_**> ')
                publisher = Publisher()
                logger.info(f' <**_**> PUBLISHER: {EXCHANGE} - {QUEUE_PUBLISHIR}')
                publisher.start_publisher(
                    message=EXCHANGE,
                    routing_name=ROUTE_KEY,
                    message=message_str, 
                    )
                publisher.close()
            except pika.exceptions.AMQPConnectionError as e:
                logger.error(f' <**_**> PUBLISHER: {e}')
                print(f"ERROR: {e}")
            
    

