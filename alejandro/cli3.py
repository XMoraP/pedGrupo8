import sys

def cli3(fifo_name):
    try:
        # Abre la FIFO para escribir la solicitud al servidor
        with open(fifo_name, "w") as fifo:
            fifo.write("Request\n")

        # Abre la FIFO para leer la respuesta del servidor
        with open(fifo_name, "r") as fifo:
            # Lee la respuesta del servidor
            server_response = fifo.readline().strip()

            # Muestra la respuesta en la salida estándar
            print("Respuesta del servidor:", server_response)

    except Exception as e:
        print("Error en el cliente:", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python cli3.py <fifo_name>")
        sys.exit(1)

    fifo_name = sys.argv[1]
    cli3(fifo_name)
