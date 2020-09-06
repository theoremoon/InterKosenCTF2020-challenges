with open("../distfiles/chall", "rb") as f:
    f.seek(0x4030)
    buf = f.read(0x20)

flag = ''
x = 0
for i in range(0x1d, -1, -1):
    c = x ^ buf[i] ^ 0xff ^ i
    flag += chr(c)
    x = c
print(flag[::-1])
