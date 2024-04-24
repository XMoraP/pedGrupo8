import os
import socket

# Obtener la dirección del socket UDS desde una variable de entorno
socket_path = os.environ.get('SOCKET_PATH', '/tmp/ped8')

# Obtener el contenido del archivo a enviar
file_content = input("Ingrese el contenido del archivo a enviar: ")

# Crear un socket UNIX y conectar al servidor
client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client_socket.connect(socket_path)

try:
    # Enviar el contenido del archivo al servidor
    client_socket.send(file_content.encode())

finally:
    # Cerrar la conexión
    client_socket.close()
