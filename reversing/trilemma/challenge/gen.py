from ptrlib import *

flag = b"KosenCTF{emperor_wins_with_a_probability_of_four-fifths}"

blocks = chunks(flag, (len(flag)+3) // 3, padding=b'\x00')
emperor, citizen, slave = blocks

def secret(addr, n):
    S = [i for i in range(0x100)]
    j = 0
    for i in range(n):
        j = (j + S[i] + ((addr >> (i%8)*8) & 0xff)) % 0x100
        S[i], S[j] = S[j], S[i]
    return S

# emperor
emperor = b"7I\x8d\xe48\x8e,\xce\x91!@\xb5\xed\xe5\xa6\x91\x93z\xc8"
S = secret(0x3fcc00000000, 0xcc)
j = 0
output = b''
for i, c in enumerate(emperor):
    i = (i + 1) % 0x100
    j = (j + S[i]) % 0x100
    S[i], S[j] = S[j], S[i]
    output += bytes([S[(S[i] + S[j]) % 0x100] ^ c])
print(output)

# citizen
S = secret(0x3f5500000000, 0x55)
j = 0
output = b''
for i, c in enumerate(citizen):
    i = (i + 1) % 0x100
    j = (j + S[i]) % 0x100
    S[i], S[j] = S[j], S[i]
    output += bytes([S[(S[i] + S[j]) % 0x100] ^ c])
print(output)

# slave
S = secret(0x3fee00000000, 0xee)
j = 0
output = b''
for i, c in enumerate(slave):
    i = (i + 1) % 0x100
    j = (j + S[i]) % 0x100
    S[i], S[j] = S[j], S[i]
    output += bytes([S[(S[i] + S[j]) % 0x100] ^ c])
print(output)

