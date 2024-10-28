import grpc
import random
import service_pb2
import service_pb2_grpc


# Definición de los arreglos
products = [
    "Silla Gamer",
    "Laptop HP",
    "Smartphone Samsung",
    "Audífonos Bluetooth",
    "Reloj Inteligente"
]

payment_gateways = ["MercadoPago", "PayPal", "Stripe", "Transferencia Bancaria"]
card_brands = ["VISA", "Mastercard", "American Express", "Discover"]
banks = [
    "Banco de Chile",
    "Banco Santander",
    "Banco Estado",
    "BCI",
    "Scotiabank"
]

shipping_address_regions = [
    "Región Metropolitana",
    "Región de Valparaíso",
    "Región del Biobío",
    "Región de La Araucanía",
    "Región de Los Lagos",
    "Región de Antofagasta",
    "Región de Coquimbo",
    "Región de O'Higgins",
    "Región del Maule",
    "Región de Aysén",
    "Región de Magallanes"
]

shipping_addresses = [
    "Av. Libertador Bernardo O'Higgins 1000, Santiago",
    "Calle San Martín 150, Valparaíso",
    "Calle Balmaceda 200, Concepción",
    "Calle Pajaritos 300, Maipú",
    "Calle Larga 450, Temuco"
]

def create_order(stub, customer_email):
    # Crear un pedido de ejemplo con datos aleatorios
    order = service_pb2.OrderRequest(
        product_name=random.choice(products),
        price=random.randint(10, 100000),  # Precio aleatorio entre 10 y 100 como entero
        payment_gateway=random.choice(payment_gateways),
        card_brand=random.choice(card_brands),
        bank=random.choice(banks),
        shipping_address_region=random.choice(shipping_address_regions),
        shipping_address=random.choice(shipping_addresses),
        customer_email=customer_email
    )

    # Enviar la solicitud al servicio de pedidos
    response = stub.CreateOrder(order)
    print("Respuesta del servidor:", response.message)

def run():
    # Conectarse al servidor gRPC
    channel = grpc.insecure_channel('producer:50051')
    stub = service_pb2_grpc.OrderServiceStub(channel)

    # Preguntar cuántos pedidos enviar
    while True:
        try:
            num_orders = int(input("¿Cuántos pedidos deseas enviar? "))
            if num_orders <= 0:
                print("Por favor, introduce un número positivo.")
                continue
            break
        except ValueError:
            print("Por favor, introduce un número válido.")

    # Opción para ingresar un correo de destino
    default_email = "your_email@example.com"
    email_input = input(f"Ingresa el correo electrónico de destino (predeterminado: {default_email}): ")
    customer_email = email_input.strip() if email_input else default_email

    # Confirmar si está seguro
    confirm = input(f"¿Estás seguro de que deseas enviar {num_orders} pedidos a {customer_email}? (s/n): ").strip().lower()
    if confirm != 's':
        print("Operación cancelada.")
        return

    # Enviar los pedidos
    for _ in range(num_orders):
        create_order(stub, customer_email)

if __name__ == '__main__':
    run()