import pika
import json
import logging

logging.info('Started Publicar')

class Publisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                credentials=pika.PlainCredentials('secedu', 'ep4X1!br')
            )
        )
        self.channel = self.connection.channel()

    def start_publisher(self, message, routing_name):
        logging.info(f'ROUTER_KEY: {routing_name}')
        self.channel.basic_publish(exchange='secedu', 
                                   routing_key=routing_name, 
                                   body=message)
        
        #print("Mensagem publicada:", message)

    def close(self):
        logging.info(f'close: <#:#> Publicar')

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
