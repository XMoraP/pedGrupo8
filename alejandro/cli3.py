import os

nombre_fifo = '/tmp/ped8'

fifo_fecha_y_hora = os.open(nombre_fifo, os.O_RDONLY)


respuesta_serv3 = os.read(fifo_fecha_y_hora, 1024).decode().strip()

print("respuesta del servidor:", respuesta_serv3)

os.close(fifo_fecha_y_hora)

os.system(f"echo 'cli3' > /proc/{os.getpid()}/comm")