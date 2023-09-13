import os
import re
import json
from datetime import datetime, timedelta
import time
from publicar import Publisher

class DeviceProcessor:
    def __init__(self, device_name):
        self.device_name = device_name
        self.ftp_folder = '../ftp'
        self.date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        self.device_register = self.get_device_register()
        self.processed_dates = set()

    def get_device_register(self):
        try:
            if os.path.exists(f'{self.device_name}.json'):
                with open(f'{self.device_name}.json', 'r') as file:
                    data = json.load(file)
                    return data
        except Exception as e:
            print(f'Error loading device register: {str(e)}')

        return {}

    def save_device_register(self):
        try:
            with open(f'{self.device_name}.json', 'w') as file:
                json.dump(self.device_register, file)
        except Exception as e:
            print(f'Error saving device register: {str(e)}')

    def get_current_date(self):
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        return current_date

    def check_interval(self, folder_date, last_processed_date):
        current_date = self.get_current_date()

        if last_processed_date is None: 
            last_processed_date = datetime(2023, 1, 1)

        if datetime.strptime(last_processed_date, "%Y-%m-%d") >= datetime.strptime(current_date, "%Y-%m-%d"):
            print(f'{self.device_name}: Já foi processado até {last_processed_date}, saltar...')
            return False

        if datetime.strptime(last_processed_date, "%Y-%m-%d") >= datetime.strptime(folder_date, "%Y-%m-%d"):
            print(f'{self.device_name}: Já processado {folder_date}, saltar...')
            return False

        if datetime.strptime(folder_date, "%Y-%m-%d") < datetime.strptime(self.device_register[self.device_name][0], "%Y-%m-%d"):
            print(f'{self.device_name}: Pasta antes do intervalo, saltando...')
            return False

        if folder_date in self.processed_dates:
            print(f'{self.device_name}: Pasta {folder_date} já processado, saltando...')
            return False

        return True

    def process_folder(self, folder):
        for root, dirs, files in os.walk(folder):
            for dir in dirs:
                if self.date_pattern.match(dir):
                    date_capture = dir
                    timestamp = datetime.now().timestamp()
                    file_path = os.path.join(root, dir)

                    if not self.check_interval(date_capture, self.device_register[self.device_name][1]):
                        continue

                    message_dict = {
                        "timestamp": timestamp,
                        "file_path": file_path,
                        "date_capture": date_capture,
                        "device_name": self.device_name
                    }

                    message_str = json.dumps(message_dict)

                    print(f'Message: {message_str}')

                    publisher = Publisher()

                    publisher.start_publisher(
                        message=message_str,
                        routing_name='path_init'
                    )
                    publisher.close()

                    self.device_register[self.device_name] = (self.device_register[self.device_name][0], date_capture)
                    self.save_device_register()

                    self.processed_dates.add(date_capture)

    def run(self):
        device_folder = os.path.join(self.ftp_folder, self.device_name)
        if not os.path.isdir(device_folder):
            return

        start_date = self.device_register.get(self.device_name, (None, None))[0]

        while True:
            current_date = self.get_current_date()

            if start_date and current_date < start_date:
                print(f'{self.device_name}: Ainda não chegou a data de início, aguardando...')
                time.sleep(60)
                continue

            if self.device_register.get(self.device_name) is None:
                self.device_register[self.device_name] = ('1900-01-01', '1900-01-01')

            last_processed_date = self.device_register.get(self.device_name)[1]

            if last_processed_date is None:
                last_processed_date = datetime(1900, 1, 1)
            else:
                last_processed_date = datetime.strptime(last_processed_date, "%Y-%m-%d")

            current_date = datetime.strptime(current_date, "%Y-%m-%d")

            if current_date > last_processed_date:
                self.process_folder(device_folder)

            time.sleep(60)

# Exemplo de uso
if __name__ == "__main__":
    device_name = "sippe1"
    processor = DeviceProcessor(device_name)
    processor.run()
