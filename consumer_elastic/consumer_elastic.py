from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

# Configuración de Kafka
KAFKA_BROKER = 'kafka:9093'
TOPIC_NAME = 'Pedidos'

# Configuración de Elasticsearch
es = Elasticsearch(['http://elasticsearch:9200'])

def main():

    # Verificar si el índice ya existe
    if not es.indices.exists(index='pedidos'):
        es.indices.create(index='pedidos')

    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        order = message.value
        # Indexar el pedido en Elasticsearch
        es.index(index='pedidos', body=order)
        print(f'Pedido indexado en Elasticsearch: {order}')

if __name__ == '__main__':
    main()
