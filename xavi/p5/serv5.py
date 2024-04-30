import socket, os, time

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serv_socket.bind(('192.168.164.138', 8008))

while True:
    data_r, address = serv_socket.recvfrom(256)
    print(address)
    if not data_r:
        break
    file = os.open(data_r.decode('utf-8'), os.O_RDONLY)
    while True: 
        data_s = os.read(file, 256)
        if not data_s:
            break
        serv_socket.sendto(data_s, address)
        time.sleep(0.1)
    os.close(file)

serv_socket.close()
