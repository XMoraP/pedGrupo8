import os
import time
from datetime import datetime

fifog8 = '/tmp/fifog8'

if not os.path.exists(fifog8):
	os.mkfifo(fifog8)

fifo_write = os.open(fifog8, os.O_WRONLY)
mensaje = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#Ejemplo para mandar varios mensajes
while True:
	os.write(fifo_write, mensaje.encode('utf-8'))
	time.sleep(0.1)	
os.close(fifo_write)