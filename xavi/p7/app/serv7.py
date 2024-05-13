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

class Server():
    def __init__(self):
        self.serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_socket.bind(('0.0.0.0', 8888))
        self.serv_socket.listen(5)

        self.clientes_pendientes = []
        self.clientes_verificados = []
        self.nuevo_usuario = []
        self.bd_usuarios = {}
        self.puerto = {}

        print("Servidor activo." + "\n" + "Esperando clientes...")

    def enviar_mensajes(self, mensaje, emisor, clientes):
        for cliente in clientes:
            if cliente != emisor:
                try:
                    cliente.send(mensaje)
                except:
                    cliente.close()
                    clientes.remove(cliente)

    def detener_servidor(self):
        print("Deteniendo el servidor...")
        mensaje_desconexion = "El servidor se ha detenido. Desconéctese por favor."
        for cliente in self.clientes_verificados:
            cliente.send(mensaje_desconexion.encode())
        self.serv_socket.close()
        sys.exit()

    def mostrar_prompt(self, login):
        return f'[{str(login)}]: '

    def auth(self, cliente_s):
        user = cliente_s.recv(1024)
        user_name = '[' + str(user.decode('utf-8')) + ']'
        recibido = 'recibido'
        cliente_s.send(recibido.encode())

        validacion = cliente_s.recv(1024).decode('utf-8').strip()

        if validacion == 200:
            if user_name in self.bd_usuarios:
                cod = 200
                cliente_s.send(cod.encode())
            else:
                cod = 200
                cliente_s.send(cod.encode())
        else:
            cliente_s.send(recibido.encode())
        passwd = cliente_s.recv(1024)
        cliente_s.send(recibido.encode())
        my_passwd = passwd.decode('utf-8')

        if user_name in self.bd_usuarios:
            if not context.verify(my_passwd, self.bd_usuarios[user_name]['passwd']):
                mensaje_para_cliente = "Contraseña incorrecta"
                cliente_s.send(mensaje_para_cliente.encode())
                cliente_s.close()
            elif user_name in self.puerto.values():
                mensaje_para_cliente = "Este usuario ya se encuentra en línea."
                cliente_s.send(mensaje_para_cliente.encode())
                cliente_s.close()
            else:
                welcome = '\nBienvenid@ ' + user_name
                prompt = self.mostrar_prompt(user.decode('utf-8'))
                cliente_s.send(prompt.encode())
                self.puerto[cliente_s.getpeername()[1]] = user_name
                cliente_s.send(welcome.encode())
                print(user.decode('utf-8'))
                self.clientes_verificados.append(cliente_s)
        else:
            ms_para_cliente = '\nBienvenid@ nuevo usuario'
            cliente_s.send(ms_para_cliente.encode())
            self.puerto[cliente_s.getpeername()[1]] = user_name
            self.bd_usuarios[user_name] = {'name': user_name, 'passwd': my_passwd}
            print(user.decode('utf-8'))
            print(self.bd_usuarios)
            self.clientes_verificados.append(cliente_s)

            prompt = self.mostrar_prompt(user.decode('utf-8'))
            cliente_s.send(prompt.encode())

    def run_server(self):
        while True:
            lectura, _, _ = select.select([self.serv_socket] + self.clientes_pendientes + self.clientes_verificados + [sys.stdin], [], [])
            
            for socket_listo in lectura:
                if socket_listo == self.serv_socket:
                    cliente_socket, cliente_addr = self.serv_socket.accept()
                    print("Nueva conexión de cliente ", cliente_addr)
                    self.clientes_pendientes.append(cliente_socket)
                elif socket_listo in self.clientes_pendientes:
                    self.auth(socket_listo)
                    self.clientes_pendientes.remove(socket_listo)
                elif socket_listo is sys.stdin:
                    comando = sys.stdin.readline().strip().lower()
                    if comando == "stop":
                        self.detener_servidor()
                else:
                    datos = socket_listo.recv(1024)
                    if datos:
                        valor = self.puerto[socket_listo.getpeername()[1]]
                        mensaje = f"{valor}: {datos.decode()}"
                        print(mensaje)
                        self.enviar_mensajes(mensaje.encode(), socket_listo, self.clientes_verificados)
                    else:
                        print("Cliente desconectado.")
                        del self.puerto[socket_listo.getpeername()[1]]
                        self.clientes_verificados.remove(socket_listo)
                        socket_listo.close()

if __name__ == "__main__":
    server = Server()
    server.run_server()
