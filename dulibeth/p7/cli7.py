import socket

socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cliente.connect(('192.168.127.139',8000)) 

while True:
    mensaje = input()
    socket_cliente.send(mensaje.enconde())
    respuesta = socket_cliente.recv(1024).decode()
    print(respuesta)
    

