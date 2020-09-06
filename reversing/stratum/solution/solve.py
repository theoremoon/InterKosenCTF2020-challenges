from z3 import *
from ptrlib import *

def encode(flag):
    tmp_meta = b''
    for i in range(len(flag)):
        popcnt = bin(flag[i])[2:].count('1')
        lzcnt  = bin(flag[i])[2:].zfill(8).find('1')
        lzcnt  = 0x10 if lzcnt == -1 else lzcnt
        x = (popcnt << 4) | lzcnt
        tmp_meta += bytes([x ^ flag[(i+0x10) % 0x40]])
    return tmp_meta

prefix = b"KosenCTF"
key = b"asdfghjklzxcvbnm"
strmap = lambda c: key.index(c)

s = Solver()
flag = [BitVec("flag{:02x}".format(i), 8) for i in range(0x40)]
for i in range(len(prefix)):
    s.add(flag[i] == prefix[i])

code = b''
meta = b''
with open("../distfiles/flag.enc", "rb") as f:
    for i in range(4):
        code += f.read(0x10)
        meta += f.read(0x10)

for i in range(len(flag)):
    s.add(Or(And(0x20 < flag[i], flag[i] < 0x7f),
             flag[i] == 0,
             flag[i] == 0x0a))
    s.add(flag[i] & 0xf == strmap(code[i]))
    popcnt = (meta[i] ^ flag[(i + 0x10) % 0x40]) >> 4
    lzcnt  = (meta[i] ^ flag[(i + 0x10) % 0x40]) & 0xf
    s.add(Or(lzcnt == 1,
             lzcnt == 2,
             And(lzcnt == 4, flag[i] == 0x0a),
             And(lzcnt == 0, flag[i] == 0x00)))
    c = flag[i]
    d = (c & 0x55) + (c >> 1 & 0x55)
    e = (d & 0x33) + (d >> 2 & 0x33)
    f = (e & 0x0f) + (e >> 4 & 0x0f)
    s.add(Or(flag[i] == 0, f == popcnt))
    s.add(Or(flag[i] != 0, f == 0))

while True:
    if s.check() == sat:
        m = s.model()
        answer = ['?' for i in range(len(flag))]
        for d in m.decls():
            answer[int(d.name()[4:], 16)] = bytes([m[d].as_long()])
        answer = b''.join(answer)
        if meta == encode(answer):
            print(answer)
        s.add(Not(And(
            [flag[int(d.name()[4:], 16)] == m[d] for d in m.decls()]
        )))
    else:
        break
