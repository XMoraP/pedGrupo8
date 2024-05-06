import socket
import select
import sys

login = sys.argv[1]

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect(('192.168.1.107', 8888))
cliente_socket.send(login.encode())

new_user = f'[' + str(login) + ']'

lista_lectura = [cliente_socket, sys.stdin]

while True:
    lectura, _, _ = select.select(lista_lectura, [], [])
    for sock in lectura:
        if sock is cliente_socket:
            mensaje = cliente_socket.recv(1024).decode()
            if not mensaje:
                print("No hay conexion.")
                sys.exit()
            else:
                print(mensaje)
        else:
            mensaje = input('[' + str(login) + ']:').strip()
            cliente_socket.send(mensaje.encode())

cliente_socket.close()
