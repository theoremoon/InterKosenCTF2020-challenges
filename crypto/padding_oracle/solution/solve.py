from ptrlib import Socket
from binascii import hexlify, unhexlify
import os

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "13004")

sock = Socket(HOST, int(PORT))
flag = unhexlify(sock.recvline())

def oracle(c):
    sock.sendline(hexlify(c))
    return sock.recvline() == b"True"

def padding_oracle_block(oracle, prev_block, block):
    plain_block = bytearray(bytes(len(prev_block)))
    for i in range(len(block)):
        for b in range(256):
            p = plain_block[:]
            for j in range(i):
                p[j] = plain_block[j] ^ prev_block[j] ^ (i+1)
            p[i] = b

            if oracle(p + block):
                plain_block[i] = (i+1) ^ prev_block[i] ^ b
                break
        else:
            raise ValueError("NOT FOUND")
    return bytes(plain_block)

def padding_oracle(oracle, ciphertext):
    cipher_blocks = []
    for i in range(0, len(ciphertext), 16):
        cipher_blocks.append(ciphertext[i:i+16])

    plaintext = b''
    for i in range(len(cipher_blocks)-1):
        plaintext += padding_oracle_block(oracle, cipher_blocks[i], cipher_blocks[i+1])
    return plaintext


print(padding_oracle(oracle, flag))
