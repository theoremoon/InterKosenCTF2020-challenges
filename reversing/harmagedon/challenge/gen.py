import random
import string

table = list(string.ascii_letters + string.digits + "{}_-")
flag = "Ruktun0rDi3"
N = 4 # number of branches
size = 0
for i in range(1, len(flag)+1):
    size += N**i
tree = [random.choice(table) for _ in range(size)]

d = 0
i = 0
while d < len(flag):
    j = random.randrange(0, N)
    args = random.sample(set(table) - set([flag[d]]), k=N)
    args[j] = flag[d]
    tree = tree[:i] + args + tree[i + N:]
    assert tree[i + j] == flag[d]
    i = (i + j + 1) * N
    d += 1

target = i
tree = "".join(tree)

f = ''
while i >= N:
    i = i // N - 1
    f += tree[i]
assert f[::-1] == flag


template = open("template.asm", "r").read()
with open("chall.asm", "w") as f:
    f.write(template.format(buf=tree, target=target, depth=len(flag)))
