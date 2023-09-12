import pika
import json
import tensorflow as tf

tf.debugging.set_log_device_placement(True)

# Place tensors on the CPU
with tf.device('/CPU:0'):
    class RabbitMQPublisher:
        def __init__(self):
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='localhost', 
                    port=5672,
                    credentials=pika.PlainCredentials('sippe', 'ep4X1!br')
                )
            )
            self.channel = self.connection.channel()

            self.queue_name = ''
            #self.channel.queue_declare(queue=self.queue_name)

        def call(self, snapshot_path, timestamp, queue_name ):

            self.queue_name = queue_name
            # Cria um dicionário com as chaves "snapshot_path", "timestamp" e "url"
            message_dict = {
                "snapshot_path": snapshot_path,
                "timestamp": timestamp, 
                }

            # Serializa o dicionário em uma string JSON
            message_str = json.dumps(message_dict)

            # Publica a mensagem na fila
            self.channel.basic_publish(exchange='secedu', routing_key=self.queue_name, body=message_str)

            print("Mensagem publicada:", message_str)

        def close(self):
            self.connection.close()


    #if __name__ == '__main__':
    #    publisher = RabbitMQPublisher()
    #    snapshot_path = "/path/to/image.png"
    #    timestamp = "2022-01-01 12:00:00"
    #    publisher.publish(snapshot_path, timestamp)
    #    publisher.close()
