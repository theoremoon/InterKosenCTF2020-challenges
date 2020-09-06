with open("chall", "rb") as f:
    buf = f.read()

# anti-ghidra
buf = buf[:5] + b'\x02' + buf[6:]

with open("chall", "wb") as f:
    f.write(buf)

import os
os.system("chmod +x chall")
