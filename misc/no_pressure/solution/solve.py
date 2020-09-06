from ptrlib import Socket
from base64 import b64decode
import os

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "10002")

attack = bytes(range(0x21, 0x7b)).decode() + "}"
flag = "KosenCTF{"

sock = Socket(HOST, int(PORT))

sock.sendlineafter("message: ", flag + " $")
sock.recvuntil("encrypted! : ")
c = b64decode(sock.recvline().strip())
threshold = len(c)

while not flag.endswith("}"):
    for s in attack:
        sock.sendlineafter("message: ", flag + s + " ")
        sock.recvuntil("encrypted! : ")
        c = b64decode(sock.recvline().strip())
        if len(c) < threshold:
            flag += s
            break
    else:
        print("[-] not found")
        break
print(flag)
