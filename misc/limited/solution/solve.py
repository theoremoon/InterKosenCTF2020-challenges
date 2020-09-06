import re
from ptrlib import crt

with open("flow.txt", "r") as f:
    flow = f.read().split('</html>\n\n')

flag = ''
pairs = {}
for request in flow:
    r = re.findall('secret%2C\+(\d+)%2C.+%25\+(\d+)', request)
    if r == []: continue
    pos = int(r[0][0])
    mod = int(r[0][1])
    c = request.count('<th scope="row">')
    if pos not in pairs: pairs[pos] = []
    pairs[pos].append((c, mod))

flag = ''
for i in range(len(pairs)):
    flag += chr(crt(pairs[i+1])[0])

print(flag)
