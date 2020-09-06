from sage.all import *
from ptrlib import *
from Crypto.Util.number import *
import gmpy2
import os

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "13001")

sock = Socket(HOST, int(PORT))

sock.recvuntil("n: ")
n = int(sock.recvline())

sock.sendlineafter("> ", "2")
sock.sendlineafter("e: ", "3")
sock.sendlineafter("m: ", "00")
sock.recvuntil("c: ")
c = int(sock.recvline(), 16)

print("[+] n: {}".format(n))
print("[+] c: {}".format(c))

m = Integer(c).nth_root(3)
assert m**3 == c

r = long_to_bytes(m)[2:]
r = long_to_bytes(((bytes_to_long(r) << 1) ^ 2) & (2**64-1))
a1 = r[0] | 2
b1 = bytes_to_long(r)
shift1 = 2 ** (len(r) * 8)

e1 = 5
sock.sendlineafter("> ", "1")
sock.sendlineafter("e: ", str(e1))
sock.recvuntil("c: ")
c1 = int(sock.recvline(), 16)

r = long_to_bytes(((bytes_to_long(r) << 1) ^ 3) & (2**64-1))
a2 = r[0] | 3
b2 = bytes_to_long(r)
shift2 = 2 ** (len(r) * 8)

e2 = 7
sock.sendlineafter("> ", "1")
sock.sendlineafter("e: ", str(e2))
sock.recvuntil("c: ")
c2 = int(sock.recvline(), 16)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a.monic()

_, x = PolynomialRing(Zmod(n), name="x").objgen()
last = None
for i in range(512):
    f1 = (x * shift1 + (a1 << i*8) + b1)**e1 - c1
    f2 = (x * shift2 + (a2 << i*8) + b2)**e2 - c2

    m = -gcd(f1, f2).coefficients()[0]
    if last != m:
        print(long_to_bytes(int(m)))
    last = m


