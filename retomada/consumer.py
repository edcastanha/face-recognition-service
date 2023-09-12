## Consumer
import pika

RABBITMQ_HOST = "localhost" 
RABBITMQ_QUEUE = "arquivos" 
ROUTE_KEY = "path_init"

class Consumer: 
    def init(self): 
        self.connection = pika.BlockingConnection( 
            pika.ConnectionParameters( 
                host=RABBITMQ_HOST, 
                port=5672, 
                credentials=pika.PlainCredentials('secedu', 'ep4X1!br') ) 
                ) 
        self.channel = self.connection.channel()

        self.queue_name = RABBITMQ_QUEUE
        self.channel.queue_declare(queue=self.queue_name, durable=True)

        self.channel.queue_bind(
            exchange='secedu',
            queue=self.queue_name,
            routing_key=ROUTE_KEY
        )

def start_consumer(self):
    self.channel.basic_consume(
        queue=self.queue_name, 
        on_message_callback=self.callback, 
        auto_ack=True)
    
    print("Esperando por mensagens...")
    self.channel.start_consuming()

def callback(self, ch, method, properties, body):
    #print(f"Mensagem recebida: {body.decode()}")
    data = body.decode()
    for dado in enumerate(data):
        print(f"Mensagem recebida: {dado}")

if __name__ == "main": 
    consumidor = Consumer() 
    consumidor.start_consuming()