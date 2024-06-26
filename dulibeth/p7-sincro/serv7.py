import select
import socket
import sys

sys.path.append('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages')
from passlib.context import CryptContext

context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=50000
)


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
puerto = {}

def mostrar_prompt(login):
   return f'[{str(login)}]: '

print("Servidor activo." + "\n" + "Esperando clientes...")

while True:
    lectura, _, _ = select.select(lista_lectura + [sys.stdin], [], [])

    for sock in lectura:

        if sock is serv_socket:
            cliente_socket, cliente_addr = serv_socket.accept()
            print("Nueva conexión de cliente ", cliente_addr)
            user = cliente_socket.recv(1024)
            my_user = '[' + str(user.decode('utf-8')) + ']'
            recibido = 'recibido'
            cliente_socket.send(recibido.encode())
            validacion = cliente_socket.recv(1024).decode('utf-8').strip()
            print(validacion)
            if validacion == 'dale': 
                if my_user in bd_usuarios:
                    cod = 'ok'
                    cliente_socket.send(cod.encode())
                else:
                    cod = 'no ok' 
                    cliente_socket.send(cod.encode())
            else:
                cliente_socket.send(recibido.encode())
            passwd = cliente_socket.recv(1024)
            print(passwd.decode('utf-8'))
            cliente_socket.send(recibido.encode())
            my_passwd = passwd.decode('utf-8')

            if my_user in bd_usuarios:
                
                if not context.verify(my_passwd, bd_usuarios[my_user]['passwd']):
                    mensaje_para_cliente = "Contraseña incorrecta"
                    cliente_socket.send(mensaje_para_cliente.encode())
                    cliente_socket.close()
                elif my_user in puerto.values():
                    mensaje_para_cliente = "Este usuario ya se encuentra en linea."
                    cliente_socket.send(mensaje_para_cliente.encode())
                    cliente_socket.close()
                elif context.verify(my_passwd, bd_usuarios[my_user]['passwd']):
                    welcome = '\nBienvenid@ ' + my_user
                    prompt = mostrar_prompt(user.decode('utf-8'))
                    cliente_socket.send(prompt.encode())
                    puerto[cliente_socket.getpeername()[1]] = my_user
                    cliente_socket.send(welcome.encode())
                    print(user.decode('utf-8'))
                    lista_lectura.append(cliente_socket)
                    clientes.append(cliente_socket)

            else:
                ms_para_cliente = '\nBienvenid@ nuevo usuario'
                cliente_socket.send(ms_para_cliente.encode())
                puerto[cliente_socket.getpeername()[1]] = my_user
                bd_usuarios[my_user] = {'name': my_user, 'passwd': my_passwd}                
                print(user.decode('utf-8'))
                print(bd_usuarios)
                lista_lectura.append(cliente_socket)
                clientes.append(cliente_socket)
                prompt = mostrar_prompt(user.decode('utf-8'))
                cliente_socket.send(prompt.encode())

        elif sock is sys.stdin:
            comando = sys.stdin.readline().strip().lower() 
            if comando == "stop":
                detener_servidor()

        else:
            datos = sock.recv(1024)
            if datos:
                valor = puerto[sock.getpeername()[1]]
                mensaje = f"{valor}: {datos.decode()}"
                print(mensaje)
                enviar_mensajes(mensaje.encode(), sock, clientes)

            else:
                print("Cliente desconectado.")
                del puerto[sock.getpeername()[1]]
                lista_lectura.remove(sock)
                clientes.remove(sock)
                sock.close()

