import grpc
from concurrent import futures
from kafka import KafkaProducer
import json
import service_pb2
import service_pb2_grpc
import time
import random
from datetime import datetime  # Importar datetime para manejar fechas y horas

KAFKA_BROKER = 'kafka:9093'     # Cambia esto según tu configuración de Kafka
TOPIC_NAME = 'Pedidos'          # Nombre del topic donde se enviarán los mensajes

class OrderService(service_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        # Crear un productor de Kafka
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializar el mensaje a JSON
        )

    def CreateOrder(self, request, context):
        # Simular el tiempo de procesamiento (latencia)
        start_time = time.time()

        # Crear un diccionario con los datos del pedido
        order = {
            "product_name": request.product_name,
            "price": request.price,
            "payment_gateway": request.payment_gateway,
            "card_brand": request.card_brand,
            "bank": request.bank,
            "shipping_address_region": request.shipping_address_region,
            "shipping_address": request.shipping_address,
            "customer_email": request.customer_email,
            "current_state": "Procesando",
            "latencia": 0.0,  # Inicialmente 0, se calculará más adelante
            "tiempo_real_entrega": 0.0,  # Inicialmente 0, se actualizará más tarde
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Agregar timestamp
        }

        # Simular un procesamiento que toma tiempo
        time.sleep(random.uniform(0, 2))  # Simula un tiempo de procesamiento de 2 segundos

        # Calcular la latencia
        order["latencia"] = time.time() - start_time  # Latencia en segundos

        # Enviar el mensaje al topic de Kafka
        self.producer.send(TOPIC_NAME, order)
        self.producer.flush()  # Asegurarse de que todos los mensajes se envíen

        # Crear y devolver la respuesta
        response = service_pb2.OrderResponse()
        response.message = "Pedido recibido y enviado a Kafka."
        return response

def serve():
    # Crear un servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50051')  # Escuchar en el puerto 50051
    server.start()
    print("Servidor de pedidos en ejecución en el puerto 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()