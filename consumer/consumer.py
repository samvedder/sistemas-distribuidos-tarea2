from kafka import KafkaConsumer, KafkaProducer
import json
import smtplib
from email.mime.text import MIMEText
import time
import random

# Configuración del consumidor
KAFKA_BROKER = 'kafka:9093'
TOPIC_NAME = 'Pedidos'
PRODUCER_TOPIC = 'Pedidos'

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def send_email(customer_email, subject, message):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'your_email@example.com'
    smtp_password = 'your_password'

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = customer_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print(f'Correo enviado a {customer_email} con éxito.')
    except Exception as e:
        print(f'Error al enviar correo a {customer_email}: {e}')

def process_order(order):
    current_state = order['current_state']
    start_time = time.time()  # Iniciar el temporizador para calcular la latencia

    # Mensaje base que incluye especificaciones del producto
    product_info = (
        f"Nombre del producto: {order['product_name']}\n"
        f"Precio: ${order['price']}\n"
        f"Pasarela de pago: {order['payment_gateway']}\n"
        f"Marca de la tarjeta: {order['card_brand']}\n"
        f"Banco: {order['bank']}\n"
        f"Dirección de envío: {order['shipping_address']}, {order['shipping_address_region']}\n"
        f"Fecha y hora de procesamiento: {order['timestamp']}\n"  # Incluir el timestamp
    )

    if current_state == 'Procesando':
        subject = 'Actualización de su pedido'
        message_body = f'Su pedido ha cambiado de estado a "Procesando".\n\n{product_info}'
        send_email(order['customer_email'], subject, message_body)
        time.sleep(random.uniform(0, 2))
        order['current_state'] = 'Preparacion'
        order['tiempo_real_entrega'] = time.time() - start_time  # Calcular tiempo real de entrega
        producer.send(PRODUCER_TOPIC, order)

    elif current_state == 'Preparacion':
        subject = 'Su pedido está en preparación'
        message_body = f'Su pedido está en preparación.\n\n{product_info}'
        send_email(order['customer_email'], subject, message_body)
        time.sleep(random.uniform(0, 2))
        order['current_state'] = 'Enviado'
        order['tiempo_real_entrega'] = time.time() - start_time  # Calcular tiempo real de entrega
        producer.send(PRODUCER_TOPIC, order)

    elif current_state == 'Enviado':
        subject = 'Su pedido ha sido enviado'
        message_body = f'Su pedido ha sido enviado y está en camino.\n\n{product_info}'
        send_email(order['customer_email'], subject, message_body)
        time.sleep(random.uniform(0, 2))
        order['current_state'] = 'Entregado'
        order['tiempo_real_entrega'] = time.time() - start_time  # Calcular tiempo real de entrega
        producer.send(PRODUCER_TOPIC, order)

    elif current_state == 'Entregado':
        subject = 'Su pedido ha sido entregado'
        message_body = f'Su pedido ha sido entregado.\n\n{product_info}'
        send_email(order['customer_email'], subject, message_body)
        time.sleep(random.uniform(0, 2))
        order['current_state'] = 'Finalizado'
        order['tiempo_real_entrega'] = time.time() - start_time  # Calcular tiempo real de entrega
        producer.send(PRODUCER_TOPIC, order)

    elif current_state == 'Finalizado':
        subject = 'Pedido finalizado'
        message_body = f'Te agradecemos por tu compra. Tu pedido ha sido finalizado.\n\n{product_info}'
        send_email(order['customer_email'], subject, message_body)

# Bucle para procesar mensajes
for message in consumer:
    order = message.value
    process_order(order)