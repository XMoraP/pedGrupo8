import socket
import select
import sys

login = sys.argv[1]

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect(('192.168.1.107', 8888))
cliente_socket.send(login.encode())

new_user = f'[' + str(login) + ']'

lista_lectura = [cliente_socket, sys.stdin]

def mostrar_prompt():
    # Imprime el prompt sin nueva línea al final.
    print(f'[{str(login)}]:', end=' ', flush=True)

while True:
    lectura, _, _ = select.select(lista_lectura, [], [])
    for sock in lectura:
        if sock is cliente_socket:
            mensaje = cliente_socket.recv(1024).decode()
            if not mensaje:
                print("Desconectando...")
                sys.exit()
            else:
                print(f"\r{mensaje}")
        else:
            mensaje = input('\n' + '[' + str(login) + ']:').strip()
            cliente_socket.send(mensaje.encode())
            mostrar_prompt()

cliente_socket.close()
