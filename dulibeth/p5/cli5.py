import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    data = 'Hola soy el cliente'
    client_socket.sendto(data.encode(), ('192.168.127.138', 8000))
    response, server_address = client_socket.recvfrom(1024)

    print(response.decode())
except KeyboardInterrupt:
    pass
finally:
    client_socket.close()
