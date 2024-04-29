import socket, os

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serv_socket.bind(('0.0.0.0', 0))

while True:
    data_r, address = serv_socket.recvfrom(1024)
    print(address)
    if not data_r:
        break
    file = os.open(data_r.decode('utf-8'), os.O_RDONLY)
    while True: 
        data_s = os.read(file, 1024)
        if not data_s:
            break
        serv_socket.sendto(address, data_s)
    os.close(file)

serv_socket.close()








