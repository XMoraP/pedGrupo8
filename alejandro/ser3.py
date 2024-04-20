import sys
import time

def serv3(fifo_name):
    try:
        # Crear la FIFO
        os.mkfifo(fifo_name)

        with open(fifo_name, "r") as fifo:
            # Lee la solicitud del cliente desde la FIFO
            client_request = fifo.readline().strip()

            # Obtén la fecha y hora del sistema
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

            # Envía la fecha y hora al cliente a través de la FIFO
            with open(fifo_name, "w") as fifo:
                fifo.write(current_time + "\n")

    except Exception as e:
        print("Error en el servidor:", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python serv3.py <fifo_name>")
        sys.exit(1)
    
    fifo_name = sys.argv[1]
    serv3(fifo_name)
