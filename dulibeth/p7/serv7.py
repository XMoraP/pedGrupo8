import select
import socket
import sys

def enviar_mensajes(mensaje, emisor, clientes):
    for cliente in clientes:
        if cliente != emisor:
            try:
                cliente.send(mensaje)
            except:
                cliente.close()
                clientes.remove(cliente)

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.bind(('192.168.127.139', 8888))
serv_socket.listen(5)

clientes = []
lista_lectura = [serv_socket]

print("Servidor activo. Esperando clientes...")

while True:
    lectura, _, _ = select.select(lista_lectura, [], [])

    for sock in lectura:
        if sock is serv_socket:
            cliente_socket, cliente_addr = serv_socket.accept()
            print("Nueva conexión de cliente", cliente_addr)
            lista_lectura.append(cliente_socket)
            clientes.append(cliente_socket)
        else:
            datos = sock.recv(1024)
            if datos:
                mensaje = f"{sock.getpeername()[0]}: {datos.decode()}"
                print(mensaje)
                enviar_mensajes(mensaje.encode(), sock, clientes)
            else:
                print(f"{sock.getpeername()[0]} desconectado.")
                lista_lectura.remove(sock)
                clientes.remove(sock)
                sock.close()