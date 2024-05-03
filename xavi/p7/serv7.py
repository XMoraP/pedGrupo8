import socket, os, sys

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_sock.bind(('0.0.0.0', 8008))

stderr = sys.stderr.fileno()

server_sock.listen(3) 

while True:
    os.write(stderr, b'Esperando conexiones\n')
    client_sock, address = server_sock.accept()
    os.write(stderr, address.encode('utf-8'))
    
    fd = client_sock.fileno()

    login = os.read(fd, 1024)
    new_user = '[' + login + ']'
    db_users = []
    for user in db_users:
        if user == new_user:
            os.write(fd, b'Nombre de usuario no disponible')
        else:
            db_users.append(str(new_user))
            user_msg = str(new_user) + 'Se ha unido al chat.\n'
            os.write(fd, user_msg.encode('utf-8'))
            break
    while True: 
        chat_msg = os.read(fd, 1024)
        if not chat_msg:
            break
        os.write(fd, chat_msg)
    


    

    




