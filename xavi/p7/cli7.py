import socket
import select
import sys
import getpass

sys.path.append('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages')
import passlib.hash as phash
from passlib.context import CryptContext

login = sys.argv[1]

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect(('192.168.164.141', 8888))
cliente_socket.send(login.encode())

passwd = getpass.getpass(prompt="Introduzca su contraseña: ")

context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=50000
)
hashed_password = context.hash(passwd)
print(context.verify("test_password", hashed_password))


print(f"Contraseña ingresada: {passwd}")
print(f"Contraseña encriptada: {hashed_password}")

cliente_socket.send(hashed_password.encode())



new_user = f'[' + str(login) + ']'

lista_lectura = [cliente_socket, sys.stdin]

def mostrar_prompt():
    # Imprime el prompt sin nueva línea al final.
    print(f'[{str(login)}]: ', end=' ', flush=True)

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
