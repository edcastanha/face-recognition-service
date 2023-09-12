import pika

class Publisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST)
            )
        self.channel = self.connection.channel()
    
    def start_publisher(self, queue, message, routing_key=''):
        self.channel.basic_publish(
            exchange='',
            routing_key=routing_key,
              body=message,
              properties=pika.BasicProperties(
                  delivery_mode=2, # Faz a mensagem persistir em caso de reinicialização do RabbitMQ
                  )
                  
    def close(self):
        self.connection.close()
