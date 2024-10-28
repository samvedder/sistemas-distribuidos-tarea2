
# Sistema de Pedidos Distribuido con gRPC y Kafka
Este proyecto implementa un sistema distribuido para la gestión y procesamiento de pedidos en un entorno de e-commerce, utilizando microservicios y tecnologías como gRPC, Kafka, y SMTP para enviar notificaciones a los clientes por correo electrónico. El sistema está diseñado para simular el flujo de pedidos, desde su creación hasta su entrega final, interactuando con servicios de pago, transporte, y notificación.

## Descripción del Proyecto

El sistema permite la creación de pedidos aleatorios que incluyen información como productos, precios, métodos de pago y detalles de envío. Los pedidos se procesan a través de Kafka, y el sistema utiliza gRPC para la comunicación entre los servicios. Además, se envían correos electrónicos a los clientes para informar sobre el estado de sus pedidos.

### Tecnologías Utilizadas:
- **gRPC**: Para la comunicación entre el cliente y el servidor.
- **Kafka**: Para manejar la cola de pedidos y la transmisión de mensajes.
- **smtplib (Python)**: Para enviar correos electrónicos a los clientes con las actualizaciones del estado del pedido.
- **Docker**: Para contenerizar los servicios.

## Requisitos previos

1. Tener **Docker** y **Docker Compose** instalados.
2. Crear un token de acceso para utilizar con GitHub si vas a clonar el proyecto desde un repositorio privado.
3. Tener una cuenta de correo electrónico válida para enviar correos (se usa Gmail en este proyecto, pero puedes adaptar la configuración a tu proveedor de correo).
4. **Python 3.x** instalado.

## Instalación y Configuración

1. Clona este repositorio en tu máquina local:
   ```bash
   git clone https://github.com/samvedder/sistemas-distribuidos-tarea2.git
   cd sistemas-distribuidos-tarea2
   ```

2. Configura tu entorno con Docker:
   - En el archivo `docker-compose.yml`, asegúrate de que las configuraciones de los servicios `kafka`, `producer`, `consumer` y `producer` estén correctas.
   - Inicia los servicios con:
     ```bash
     docker-compose up --build
     ```

3. Configura los correos electrónicos para el envío de notificaciones en `consumer.py`:
   - Necesitas cambiar los valores por defecto de `smtp_user` y `smtp_password` en la función `send_email` por tu propio correo y una contraseña.
   - Puedes configurar un correo alternativo si no utilizas Gmail, actualizando los valores de `smtp_server` y `smtp_port`.


4. (Opcional) Puedes modificar los productos, métodos de pago y otros detalles en `client.py` según tus preferencias.

## Uso del Sistema
## Dockers
### Levantar contenedores
  ```bash
  sudo docker-compose -f docker-compose.network.yml -f docker-compose.ApacheKafka.yml -f docker-compose.Elasticsearch.yml -f docker-compose.admin.yml -f docker-compose.client.yml -f docker-compose.producer.yml -f docker-compose.consumer.yml up --build
  ```
### Bajar contenedores
  ```bash
  sudo docker-compose -f docker-compose.network.yml -f docker-compose.ApacheKafka.yml -f docker-compose.Elasticsearch.yml -f docker-compose.admin.yml -f docker-compose.client.yml -f docker-compose.producer.yml -f docker-compose.consumer.yml down -v
  ```
### Entrar cliente gRPC
  ```bash
  sudo docker exec -it client bash
  ```
### Cliente gRPC
1. El archivo `client.py` genera pedidos aleatorios que se envían a través de gRPC. Ejecuta el cliente de la siguiente manera:
   ```bash
   python3 client.py
   ```

2. El cliente te preguntará cuántos pedidos deseas generar y enviar. También podrás ingresar el correo electrónico del cliente que recibirá las notificaciones.

### Consumidor Kafka
El archivo `consumer.py` escucha en el tópico de Kafka y procesa los pedidos. Cambia el estado de cada pedido y envía un correo electrónico al cliente en cada etapa del proceso (procesando, en preparación, enviado, entregado, finalizado).

- El consumidor se ejecuta automáticamente dentro de Docker y procesa los pedidos que llegan al tópico `Pedidos` de Kafka.

## Flujo del Sistema

1. El **cliente gRPC** envía un pedido al servidor.
2. El servidor envía el pedido al tópico de **Kafka**.
3. El **consumidor Kafka** escucha los pedidos entrantes y procesa cada uno, cambiando su estado y enviando correos electrónicos al cliente para actualizarlo.
4. El sistema procesa el pedido en las siguientes etapas: `Procesando`, `Preparación`, `Enviado`, `Entregado` y `Finalizado`.

## Variables Modificables
En el archivo `client.py`, puedes personalizar los siguientes datos:
- **Lista de productos**: Puedes agregar o modificar los productos en el arreglo `products`.
- **Gateways de pago**: La lista `payment_gateways` contiene los métodos de pago disponibles.
- **Bancos**: Los bancos para las transacciones se encuentran en `banks`.
- **Direcciones de envío**: Puedes modificar las regiones y direcciones de envío en los arreglos `shipping_address_regions` y `shipping_addresses`.
