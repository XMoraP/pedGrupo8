import os
import sys 
from datetime import datetime


fd = os.open('/tmp/my_fifo_g8', os.O_WRONLY)

datetime = datetime.now()
datetime_bytes = datetime.isoformat()

os.write(fd, datetime_bytes.encode('utf-8'))

os.close(fd)