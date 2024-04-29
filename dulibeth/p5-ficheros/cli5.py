import socket

host = "192.168.127.139"
port = 8000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(str.encode("/etc/services"), (host, port))

while True:
    file_chunk, addr = sock.recvfrom(2048)
    if not file_chunk:
        break
    print(file_chunk.decode(), end="") 

sock.close()

