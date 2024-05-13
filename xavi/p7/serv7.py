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
    for cliente in clientes_verificados:
        cliente.send(mensaje_desconexion.encode())
    serv_socket.close()
    sys.exit()

def auth(cliente_s):
    user = cliente_s.recv(1024)
    my_user = '[' + str(user.decode('utf-8')) + ']'
    recibido = 'recibido'
    cliente_s.send(recibido.encode())

    validacion = cliente_s.recv(1024).decode('utf-8').strip()

    if validacion == 'dale':
        if my_user in bd_usuarios:
            cod = 'ok'
            cliente_s.send(cod.encode())
        else:
            cod = 'no ok'
            cliente_s.send(cod.encode())
    else:
        cliente_s.send(recibido.encode())
    passwd = cliente_s.recv(1024)
    cliente_s.send(recibido.encode())
    my_passwd = passwd.decode('utf-8')

    if my_user in bd_usuarios:
        if not context.verify(my_passwd, bd_usuarios[my_user]['passwd']):
            mensaje_para_cliente = "Contraseña incorrecta"
            cliente_s.send(mensaje_para_cliente.encode())
            cliente_s.close()
        elif my_user in puerto.values():
            mensaje_para_cliente = "Este usuario ya se encuentra en línea."
            cliente_s.send(mensaje_para_cliente.encode())
            cliente_s.close()
        else:
            welcome = '\nBienvenid@ ' + my_user
            prompt = mostrar_prompt(user.decode('utf-8'))
            cliente_s.send(prompt.encode())
            puerto[cliente_s.getpeername()[1]] = my_user
            cliente_s.send(welcome.encode())
            print(user.decode('utf-8'))
            clientes_verificados.append(cliente_s)
    else:
        ms_para_cliente = '\nBienvenid@ nuevo usuario'
        cliente_s.send(ms_para_cliente.encode())
        puerto[cliente_s.getpeername()[1]] = my_user
        bd_usuarios[my_user] = {'name': my_user, 'passwd': my_passwd}
        print(user.decode('utf-8'))
        print(bd_usuarios)
        clientes_verificados.append(cliente_s)

        prompt = mostrar_prompt(user.decode('utf-8'))
        cliente_s.send(prompt.encode())

def mostrar_prompt(login):
   return f'[{str(login)}]: '

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.bind(('0.0.0.0', 8888))
serv_socket.listen(5)

clientes_pendientes = []
clientes_verificados = []
nuevo_usuario = []
bd_usuarios = {}
puerto = {}

print("Servidor activo." + "\n" + "Esperando clientes...")

while True:
    lectura, _, _ = select.select([serv_socket] + clientes_pendientes + clientes_verificados + [sys.stdin], [], [])
    
    for socket_listo in lectura:
        if socket_listo == serv_socket:
            cliente_socket, cliente_addr = serv_socket.accept()
            print("Nueva conexión de cliente ", cliente_addr)
            clientes_pendientes.append(cliente_socket)
        elif socket_listo in clientes_pendientes:
            auth(socket_listo)
            clientes_pendientes.remove(socket_listo)
        elif socket_listo is sys.stdin:
            comando = sys.stdin.readline().strip().lower()
            if comando == "stop":
                detener_servidor()
        else:
            datos = socket_listo.recv(1024)
            if datos:
                valor = puerto[socket_listo.getpeername()[1]]
                mensaje = f"{valor}: {datos.decode()}"
                print(mensaje)
                enviar_mensajes(mensaje.encode(), socket_listo, clientes_verificados)
            else:
                print("Cliente desconectado.")
                del puerto[socket_listo.getpeername()[1]]
                clientes_verificados.remove(socket_listo)
                socket_listo.close()
