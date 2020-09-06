from ptrlib import *
from Crypto.Util.number import *
import os

query = b"w" * 8

HOST = os.getenv("HOST", "localhsot")
PORT = os.getenv("PORT", "13003")

sock = Socket(HOST, int(PORT))
sock.sendlineafter("query: ", query)
cs = eval(sock.recvlineafter("yoshiking: ").decode())

queryseq = bin(bytes_to_long(query))[2:]
zeros = []
ones = []
for i in range(len(queryseq)):
    if queryseq[i] == '0':
        zeros.append(cs[i])
    else:
        ones.append(cs[i])

additional_zeros = []
additional_ones = []
for i in range(len(queryseq)):
    for j in range(i+1, len(queryseq)):
        if queryseq[i] == queryseq[j]:
            additional_zeros.append(cs[i] * cs[j])
        else:
            additional_ones.append(cs[i] * cs[j])

zeros += additional_zeros
ones += additional_ones

keyword = b"yoshiking, give me ur flag"
keywordseq = bin(bytes_to_long(keyword))[2:]
token = []
for i in range(len(keywordseq)):
    if keywordseq[i] == '0':
        bit, zeros = zeros[0], zeros[1:]
    else:
        bit, ones = ones[0], ones[1:]
    token.append(bit)

sock.sendlineafter("your token: ", str(token))
print(sock.recvline())
print(sock.recvline())
