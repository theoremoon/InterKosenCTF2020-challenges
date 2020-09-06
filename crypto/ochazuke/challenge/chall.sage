from Crypto.Util.number import bytes_to_long
from binascii import unhexlify
from hashlib import sha1
import re

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

def verify(public_key, message, signature):
    r, s = signature[0], signature[1]
    if r == 0 or s == 0:
        return False
    z = Zn(bytes_to_long(message))
    u1, u2 = z / s, r / s
    K = ZZ(u1) * G + ZZ(u2) * public_key
    if K == 0:
        return False
    return Zn(K[0]) == r

if __name__=="__main__":
    from secret import flag, d
    public_key = ZZ(d) * G
    print("public key:", public_key)
    
    your_msg = unhexlify(input("your message(hex): "))
    if len(your_msg) < 10 or b"ochazuke" in your_msg:
        print("byebye")
        exit()
    your_sig = sign(d, your_msg)
    print("your signature:", your_sig)

    sig = input("please give me ochazuke's signature: ")
    r, s = map(Zn, re.compile("\((\d+), (\d+)\)").findall(sig)[0])
    if verify(public_key, b"ochazuke", (r, s)):
        print("thx!", flag)
    else:
        print("it's not ochazuke :(")
