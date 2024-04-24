import os
import socket

# Obtener la dirección del socket UDS desde una variable de entorno
socket_path = os.environ.get('SOCKET_PATH', '/tmp/ped8')

# Crear un socket UNIX, enlazar y escuchar en la dirección especificada
server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_socket.bind(socket_path)
server_socket.listen(5)

print("Servidor en espera de conexiones...")

while True:
    # Aceptar la conexión del cliente
    connection, client_address = server_socket.accept()

    try:
        print("Conexión establecida desde:", client_address)

        # Recibir el contenido del archivo del cliente y mostrarlo en el servidor
        while True:
            data = connection.recv(1024)
            if not data:
                break
            print(data.decode(), end="")

    finally:
        # Cerrar la conexión
        connection.close()
