from ptrlib import *

exec(open("output.txt").read().strip())

m = common_modulus_attack([c1, c2], [e1, e2], n1)
print(bytes.fromhex(hex(m)[2:]))
