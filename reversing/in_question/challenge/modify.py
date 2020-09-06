from pwn import ELF
import os
import random
import string

def randstr(n):
    return ''.join([random.choice(string.ascii_letters[:-6]) for i in range(n)])

elf = ELF("./chall")

symbols = elf.symbols
for key in symbols:
    if len(key) == 0: continue
    new = "?" * len(key)
    os.system("./Mod-ELF-Symbol/mod-elf-symbol -o ./chall -c {} --completestr={} > /dev/null".format(key, new))
