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

def detener_servidor():
    print("Deteniendo el servidor...")
    mensaje_desconexion = "El servidor se ha detenido. Desconéctese por favor."
    for cliente in clientes:
        cliente.send(mensaje_desconexion.encode())
    serv_socket.close()
    sys.exit()

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.bind(('0.0.0.0', 8888))
serv_socket.listen(5)

clientes = []
lista_lectura = [serv_socket]

bd_usuarios = {}

print("Servidor activo. Esperando clientes...")

while True:
    lectura, _, _ = select.select(lista_lectura + [sys.stdin], [], [])

    for sock in lectura:
        if sock is serv_socket:
            cliente_socket, cliente_addr = serv_socket.accept()
            print("Nueva conexión de cliente ", cliente_addr)
            user = cliente_socket.recv(1024)
            bd_usuarios[cliente_socket.getpeername()[1]] = '\n[' + str(user.decode('utf-8')) + ']:'
            print(user.decode('utf-8'))
            lista_lectura.append(cliente_socket)
            clientes.append(cliente_socket)
        elif sock is sys.stdin:
            comando = sys.stdin.readline().strip().lower()
            if comando == "stop":
                detener_servidor()
        else:
            datos = sock.recv(1024)
            if datos:
                valor = bd_usuarios[sock.getpeername()[1]]
                mensaje = f"{valor}: {datos.decode()}"
                print(mensaje)
                enviar_mensajes(mensaje.encode(), sock, clientes)
            else:
                print("Cliente desconectado.")
                lista_lectura.remove(sock)
                clientes.remove(sock)
                sock.close()