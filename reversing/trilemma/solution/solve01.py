from ptrlib import *

def secret(addr, n):
    S = [i for i in range(0x100)]
    j = 0
    for i in range(n):
        j = (j + S[i] + ((addr >> (i%8)*8) & 0xff)) % 0x100
        S[i], S[j] = S[j], S[i]
    return S

flag = b''

elf = ELF("../distfiles/libemperor.so")
with open("../distfiles/libemperor.so", "rb") as f:
    f.seek(elf.symbol("emperor_enc") - 0x200000)
    emperor = f.read(0x13)
S = secret(0x3fcc00000000, 0xcc)
j = 0
for i, c in enumerate(emperor):
    i = (i + 1) % 0x100
    j = (j + S[i]) % 0x100
    S[i], S[j] = S[j], S[i]
    flag += bytes([S[(S[i] + S[j]) % 0x100] ^ c])

elf = ELF("../distfiles/libcitizen.so")
with open("../distfiles/libcitizen.so", "rb") as f:
    f.seek(elf.symbol("citizen_enc") - 0x200000)
    emperor = f.read(0x13)
S = secret(0x3f5500000000, 0x55)
j = 0
for i, c in enumerate(emperor):
    i = (i + 1) % 0x100
    j = (j + S[i]) % 0x100
    S[i], S[j] = S[j], S[i]
    flag += bytes([S[(S[i] + S[j]) % 0x100] ^ c])

elf = ELF("../distfiles/libslave.so")
with open("../distfiles/libslave.so", "rb") as f:
    f.seek(elf.symbol("slave_enc") - 0x200000)
    emperor = f.read(0x13)
S = secret(0x3fee00000000, 0xee)
j = 0
for i, c in enumerate(emperor):
    i = (i + 1) % 0x100
    j = (j + S[i]) % 0x100
    S[i], S[j] = S[j], S[i]
    flag += bytes([S[(S[i] + S[j]) % 0x100] ^ c])

print(flag)
