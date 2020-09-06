import os
import signal
from binascii import unhexlify, hexlify
from Crypto.Util.number import *
from flag import flag

r = os.urandom(8)
nonce = 1

p = getPrime(256)
q = getPrime(256)
n = p * q
es = set()

def pad(x: bytes) -> bytes:
    global r, nonce
    y = long_to_bytes(r[0] | nonce) + x + r

    nonce += 1
    r = long_to_bytes(((bytes_to_long(r) << 1) ^ nonce) & (2**64 - 1))
    return y

def encrypt(m: bytes, e: int) -> bytes:
    m_ = bytes_to_long(pad(m))
    return long_to_bytes(pow(m_, e, n))

MENU = """
1. Encrypt the flag
2. Encrypt your message
3. EXIT
"""

signal.alarm(30)
print("n: {}".format(n))

while True:
    print(MENU)
    choice = input("> ")
    if choice not in ["1", "2"]:
        break

    e = int(input("e: "))
    if not(3 <= e <= 65537):
        print("[-] invalid e")
        break

    if e in es:
        print("[-] e already used")
        break

    if choice == "1":
        m = flag
    if choice == "2":
        m = unhexlify(input("m: "))

    c = encrypt(m, e)
    print("c: {}".format(hexlify(c).decode()))

    es.add(e)

