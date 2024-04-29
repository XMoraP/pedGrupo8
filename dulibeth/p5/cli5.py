import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = 'Hola soy el cliente'
client_socket.sendto(data.encode(), ('192.168.127.139', 8000))