import socket
import os

host = "192.168.127.139"
port = 8000

sock_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_server.bind((host, port))
print("Servidor udp esperando clientes...")

while True:
    data, addr = sock_server.recvfrom(1024)
    file_path = data.decode("utf-8")
    print("Conexión de cliente: ", addr)
    print("Ruta del archivo recibida:", file_path)

    try:
        with open(file_path, 'rb') as file:
            while True:
                file_chunk = file.read(1024)
                if not file_chunk:
                    sock_server.sendto(b"", addr)
                    break
                sock_server.sendto(file_chunk, addr)
                print("Fragmento enviado al cliente.")
            print("Archivo completo enviado al cliente.")  
    except FileNotFoundError:
        print("El archivo no existe en la ruta proporcionada.")
