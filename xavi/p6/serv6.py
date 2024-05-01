import socket, os, sys 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('192.168.164.141', 8000))

server_socket.listen(3)

stderr = sys.stderr.fileno()

while True:
    connection, address = server_socket.accept()
    os.write(stderr, str(address).encode('utf-8')  + b'\n')

    fd = connection.fileno()

    file = os.read(fd, 1024)
    fd_file = os.open(file, os.O_RDONLY)
    while True:
        data = os.read(fd_file, 1024)
        if not data:
            break
        os.write(fd, data)
    os.close(fd_file)
    connection.close()
server_socket.close()
