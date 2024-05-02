import socket

socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.bind(('192.168.127.139',8000))
socket_servidor.listen()

while True:
    conexion, addr = socket_servidor.accept()
    print("Se ha conectado el cliente", addr)
    while True:
        mensaje_cliente = conexion.recv(1024).decode()
        print(mensaje_cliente)
        conexion.send(input().encode())
    