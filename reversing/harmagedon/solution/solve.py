data = open("harmagedon", "rb").read()
bufoffset = 0x23F
buf = data[bufoffset:]

congratz = 0xB77C7C
p = congratz
flag = ''
while p > 4:
    p = p // 4 - 1
    flag += chr(buf[p])
print("KosenCTF{{{}}}".format(flag[::-1]))
