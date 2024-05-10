import socket
import select
import sys
import getpass

sys.path.append('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages')
import passlib.hash as phash

login = sys.argv[1]

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect(('192.168.164.141', 8888))
cliente_socket.send(login.encode())

passwd = getpass.getpass(prompt="Introduzca su contraseña: ")
my_hash = phash.bcrypt
passwd_hash = my_hash.hash(passwd)


print(f"Contraseña ingresada: {passwd}")
print(f"Contraseña encriptada: {passwd_hash}")

cliente_socket.send(passwd_hash.encode())



new_user = f'[' + str(login) + ']'

lista_lectura = [cliente_socket, sys.stdin]

def mostrar_prompt():
    # Imprime el prompt sin nueva línea al final.
    print(f'[{str(login)}]\n', end=' ', flush=True)

while True:
    lectura, _, _ = select.select(lista_lectura, [], [])
    for sock in lectura:
        if sock is cliente_socket:
            mensaje = cliente_socket.recv(1024).decode()
            if not mensaje:
                print("Desconectando...")
                sys.exit()
            else: 
                print(f'\r{mensaje}')
        else:
            mostrar_prompt()
            mensaje = input().strip()
            cliente_socket.send(mensaje.encode())

cliente_socket.close()
