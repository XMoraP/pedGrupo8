import os
import sys
import time

r, w = os.pipe()
pid = os.fork()
fichero = sys.argv[1]

if pid:
    os.close(r)
    with open(fichero, "r") as f:
        contenido = f.read()
    os.write(w, contenido.encode('utf-8'))

    os.close(w)
else:
    os.close(w)
    info = f"[{os.getppid()}] cli2\n[{os.getpid()}] serv2\n"
    os.write(sys.stderr.fileno(), info.encode('utf-8'))
    while True:
        data = os.read(r, 512)
        if not data:
            break
        os.write(sys.stdout.fileno(), data)
    os.close(r)
