import os
import subprocess

def main():
    fifo_name = "/tmp/ped8_fifo"

    # Iniciar el servidor como un proceso independiente
    server_process = subprocess.Popen(["python", "serv3.py", fifo_name])

    # Iniciar el cliente como un proceso independiente
    client_process = subprocess.Popen(["python", "cli3.py", fifo_name])

    # Esperar a que ambos procesos terminen
    client_process.wait()
    server_process.wait()

if __name__ == "__main__":
    main()
