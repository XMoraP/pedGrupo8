import socket, os, sys, select

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_sock.bind(('0.0.0.0', 8008))

stderr = sys.stderr.fileno()

server_sock.listen(3) 
os.write(stderr, b'Esperando conexiones\n')

fd_server = server_sock.fileno()

rlist = [fd_server]
wlist = []

ready_read, ready_write, _ = select.select(rlist, wlist, [], None)
        
while True:
    client_sock, address = server_sock.accept()
    os.write(stderr, str(address).encode('utf-8')+b'\n')
    
    fd = client_sock.fileno()

    rlist.append(fd)

    login = os.read(fd, 1024)
    new_user = f'[' + str(login) + ']'
    os.write(stderr, new_user.encode('utf-8'))
    db_users = ['user']
    print('no he entrado en el for')
    for user in db_users:
        print('he entrado en el for')
        print(user)
        print(login.decode('utf-8'))
        if user == login.decode('utf-8'):
            os.write(fd, b'Nombre de usuario no disponible\n')
        else:
            db_users.append(str(new_user))
            user_msg = str(new_user) + 'Se ha unido al chat.\n'
            os.write(fd, user_msg.encode('utf-8'))
            print('estoy aqui')
            break
    while True: 
        chat_msg = os.read(fd, 1024)
        if not chat_msg:
            break
        os.write(fd, chat_msg)
    


    

    




