import os
import time
from datetime import datetime

fifo = '/tmp/fifo_p3'

if not os.path.exists(fifo):
	os.mkfifo(fifo)

fifo_write = os.open(fifo, os.O_WRONLY)
mensaje = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#Ejemplo para mandar varios mensajes
while True:
	os.write(fifo_write, mensaje.encode('utf-8'))
	time.sleep(0.1)
os.close(fifo_write)