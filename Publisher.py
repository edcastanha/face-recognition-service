import pika
import json

class Publisher:
    def __init__(self):
        # RabbitMQ
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                credentials=pika.PlainCredentials('secedu', 'ep4X1!br')
            )
        )
        self.channel = self.connection.channel()

    def start_publisher(self, message, timestamp, queue_name):
       
        self.channel.basic_publish(exchange='secedu', 
                                   routing_key=queue_name, 
                                   body=message)
        
        print("Mensagem publicada:", message)

    def close(self):
        self.connection.close()

#if __name__ == '__main__':
#   
#    message = "/path/to/image.png"
#    timestamp = "2022-01-01 12:00:00"
#    queue_name = 'path_init'
#    capture_date = "2022-01-01"
#    device = "camera01"
#
#    # Configurações do Redis
#    redis_host = 'localhost'
#    redis_port = 6379
#
#    publisher = Publisher()
#    publisher.start_publisher(message, timestamp, queue_name)
#    publisher.close()
