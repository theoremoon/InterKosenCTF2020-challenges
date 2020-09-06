from Crypto.Cipher import AES
from binascii import hexlify, unhexlify
from flag import flag
import os
import signal

def pad(m: bytes) -> bytes:
    l = 16 - len(m) % 16
    return bytes([l]) * l + m

def unpad(m: bytes) -> bytes:
    l = m[0]
    assert 1 <= l <= 16
    assert bytes([l]) * l == m[:l]
    return m[l:]

def main():
    key = os.urandom(16)
    iv = os.urandom(16)
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    cipher = aes.encrypt(pad(flag))
    print(hexlify(iv + cipher).decode())

    signal.alarm(1200)
    while True:
        c = unhexlify(input())
        try:
            iv, c = c[:16], c[16:]
            m = AES.new(key=key, mode=AES.MODE_CBC, iv=iv).decrypt(c)
            u = unpad(m)
            print(True)
        except:
            print(False)


if __name__ == '__main__':
    main()
