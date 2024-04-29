import socket, os , sys

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

file = sys.argv[1]

my_socket.connect(('localhost',8080))
fd = my_socket.fileno()

info = f"[{os.getpid()}]cli4: Conectado\n"
os.write(sys.stderr.fileno(), info.encode('utf-8'))

os.write(fd, file.encode('utf-8'))
while True: 
    response = os.read(fd, 512)
    if response == f'El fichero no existe':
        os.write(sys.stdout.fileno(), response)
        os.close(fd)                                                 
    if not response:
        break
    os.write(sys.stdout.fileno(), response)                                                 

os.close(fd)


