import socket
import select
import sys

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect(('192.168.127.139', 8888))

lista_lectura = [cliente_socket, sys.stdin]
print("Empiece a escribir mensajes:")
while True:
    lectura, _, _ = select.select(lista_lectura, [], [])
    for sock in lectura:
        if sock is cliente_socket:
            mensaje = cliente_socket.recv(1024).decode()
            if not mensaje:
                print("Se perdió la conexión con el servidor.")
                sys.exit()
            else:
                print(mensaje)
        else:
            mensaje = input()
            cliente_socket.send(mensaje.encode())

cliente_socket.close()
