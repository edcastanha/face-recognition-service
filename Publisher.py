import pika
import json
import redis

class Publisher:
    def __init__(self, host, port, username, password, redis_host, redis_port):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
                credentials=pika.PlainCredentials(username, password)
            )
        )
        self.channel = self.connection.channel()
        self.queue_name = ''
        self.redis_client = redis.Redis(host=redis_host, port=redis_port)

    def start_publisher(self, snapshot_path, timestamp, queue_name, capture_date, device):
        self.queue_name = queue_name
        message_dict = {
            "snapshot_path": snapshot_path,
            "timestamp": timestamp,
            "capture_date": capture_date,
            "device": device
        }
        message_str = json.dumps(message_dict)
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message_str)
        print("Mensagem publicada:", message_str)

        # Log no Redis
        self.redis_client.hmset("mensagem_processada", {
            "data_processamento": timestamp,
            "conteudo": message_str,
            "origem": self.queue_name,
            "destinatario": "seu_destinatario",
            "status_processamento": "pendente"
        })

    def close(self):
        self.connection.close()

if __name__ == '__main__':
    host = 'localhost'
    port = 5672
    username = 'sippe'
    password = 'ep4X1!br'
    snapshot_path = "/path/to/image.png"
    timestamp = "2022-01-01 12:00:00"
    queue_name = 'secedu'
    capture_date = "2022-01-01"
    device = "camera01"

    # Configurações do Redis
    redis_host = 'localhost'
    redis_port = 6379

    publisher = Publisher(host, port, username, password, redis_host, redis_port)
    publisher.start_publisher(snapshot_path, timestamp, queue_name, capture_date, device)
    publisher.close()
