import os 

nombre_fifo = '/tmp/ped8'

if not os.path.exists(nombre_fifo):
    os.mkfifo(nombre_fifo)