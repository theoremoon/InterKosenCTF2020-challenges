from Crypto.Util.number import inverse, bytes_to_long
from ptrlib import Socket
from hashlib import sha1
from binascii import hexlify
import re
import os

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "13005")

EC = EllipticCurve(
    GF(0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff),
    [-3, 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b]
)
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551 # EC.order()
Zn = Zmod(n)
G = EC((0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
        0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5))

def sign(private_key, message):
    z = Zn(bytes_to_long(message))
    k = Zn(ZZ(sha1(message).hexdigest(), 16)) * private_key
    assert k != 0
    K = ZZ(k) * G
    r = Zn(K[0])
    assert r != 0
    s = (z + r * private_key) / k
    assert s != 0
    return (r, s)

sock = Socket(HOST, int(PORT))

sock.recvuntil("public key: ")
pubkey = EC(list(map(int, re.compile(r"(\d+) : (\d+) : 1").findall(sock.recvline().decode())[0])))
print("[+] pubkey:", pubkey)

msg = open("./shattered-1.pdf", "rb").read(320)
sock.sendlineafter("your message(hex): ", hexlify(msg))
sock.recvuntil("your signature: ")
sig = eval(sock.recvline().decode().strip())
print("[+] sig:", sig)
sock.close()

msg2 = open("./shattered-2.pdf", "rb").read(320)
print(sha1(msg).hexdigest(), sha1(msg2).hexdigest())

sock = Socket(HOST, int(PORT))
sock.sendlineafter("your message(hex): ", hexlify(msg2))
sock.recvuntil("your signature: ")

sig2 = eval(sock.recvline().decode().strip())
print("[+] sig2:", sig2)

n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
k = ((bytes_to_long(msg) - bytes_to_long(msg2)) * inverse(sig[1] - sig2[1], n)) % n
d = ((sig[1] * k  - bytes_to_long(msg)) * inverse(sig[0], n)) % n

print("[+] k:", k)
print("[+] d:", d)

assert ZZ(d) * G == pubkey

ans = sign(d, b"ochazuke")
sock.sendlineafter("ochazuke's signature: ", str(ans))
print(sock.recvline())
