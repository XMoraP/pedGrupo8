import socket, os, sys 

cli_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

address = ('localhost', 8008)

file = sys.argv[1]

fd = cli_socket.fileno()

cli_socket.sendto(file.encode('utf-8'), address)

while True: 
    data = os.read(fd, 1024)
    if not data:
        break
    os.write(sys.stdout.fileno() ,data)
os.close(fd)
