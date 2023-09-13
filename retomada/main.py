import os
import re
import json
from datetime import datetime

from publicar import Publisher

# Configurar a pasta FTP
ftp_folder = '../ftp'

# Expressão regular para o padrão AAAA-MM-DD
date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

# Percorrer a pasta FTP
for root, dirs, files in os.walk(ftp_folder):
    for dir in dirs:
        # Verificar se a subpasta corresponde ao padrão AAAA-MM-DD
        if date_pattern.match(dir):
            components = root.split('/')
            device_name = components[2]
            date_capture = dir
            file_path = os.path.join(root, dir)
            timestamp = datetime.now().timestamp()

            message_dict = {
                "timestamp": timestamp,
                "file_path": file_path,
                "date_capture": date_capture,
                "device_name": device_name
            }

            message_str = json.dumps(message_dict)
            # print(f"{date_capture} : {device_name}")
            # Chamar o Publisher para enviar a mensagem à fila
            publisher = Publisher()
            # file_path, date_capture, device_name
            # Obter o timestamp atual
            publisher.start_publisher(
                message=message_str, 
                timestamp=timestamp, 
                queue_name='path_init'
                )
            publisher.close()
