import socket

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv_socket.bind('192.168.127.139', 8000)
data = serv_socket.recv(1024)
print(data)
