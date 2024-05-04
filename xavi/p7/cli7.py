import socket, os, sys

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_sock.connect(('192.168.164.141', 8008))

user = sys.argv[1]

stdout = sys.stdout.fileno()

fd = client_sock.fileno()
os.write(fd, user.encode('utf-8'))

out = False

while not out:
    chat_output =  os.read(fd, 1024)
    os.write(stdout, chat_output)
    chat_input = input('>>>[' + user + ']:')
    if chat_input.lower() == 'salir':
        os.write(stdout, b'Saliendo del chat...')
        out = True
        os.close(fd)
    else:
        os.write(fd, chat_input.encode('utf-8')+b'\n')

