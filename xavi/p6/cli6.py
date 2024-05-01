import socket, os, sys 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address = sys.argv[1]
client_socket.bind((address))

file = sys.argv[2]
fd = client_socket.fileno()

stdout = sys.stdout.fileno()

os.wrtie(fd, file.encode('utf-8'))

while True:
    data = os.read(fd, 1024)
    if not data: 
        break
    os.write(stdout, data)
    
os.close(fd)
client_socket.close()
