import os 
import time

nombre_fifo = '/tmp/ped8'

if not os.path.exists(nombre_fifo):
    os.mkfifo(nombre_fifo)


fifo_fecha_y_hora = os.open(nombre_fifo, os.O_WRONLY)

current_time = time.strftime("%Y-%m-%d %H:%M:%S" + "\n", time.localtime())

os.write(fifo_fecha_y_hora , current_time.encode())

os.close(fifo_fecha_y_hora)
