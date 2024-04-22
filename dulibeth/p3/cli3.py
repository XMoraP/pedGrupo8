import os
import sys

#Abro la fifo
fifo_read = os.open('/tmp/fifo_p3', os.O_RDONLY)

#Ejemplo si tengo varios mensajes
while True:
	mensaje = os.read(fifo_read, 1024).decode('utf-8')
	if mensaje:	
		sys.stdout.write("Fecha y hora: " + mensaje + "\n")
	else:
		break
os.close(fifo_read)


