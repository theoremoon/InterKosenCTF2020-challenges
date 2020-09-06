from Crypto.Util.number import *
from secret import flag

def legendre_symbol(x, p):
    a = pow(x, (p-1) // 2, p)
    if a == 0:
        return 0
    elif a == 1:
        return 1
    else:
        return -1

def key_gen(bits):
    p = getPrime(bits)
    q = getPrime(bits)
    n = p * q

    while True:
        z = getRandomRange(2, n)
        a, b = legendre_symbol(z, p), legendre_symbol(z, q)
        if a == -1 and b == -1:
            break

    return (n, z), (p, q)

def enc(pubkey, m):
    n, z = pubkey
    bits = [int(b) for b in "{:b}".format(m)]

    c = []
    for b in bits:
        while True:
            x = getRandomRange(2, n)
            if GCD(x, n) == 1:
                break
        c.append( ((z**b) * (x**2)) % n )
    return c

def dec(privkey, c):
    p, q = privkey
    m = ""
    for b in c:
        if legendre_symbol(b, p) == 1 and legendre_symbol(b, q) == 1:
            m += "0"
        else:
            m += "1"
    return int(m, 2)

def main():
    pubkey, privkey = key_gen(256)

    keyword = "yoshiking, give me ur flag"
    m = input("your query: ")
    if any([c in keyword for c in m]):
        print("yoshiking: forbidden!")
        exit()

    if len(m) > 8:
        print("yoshiking: too long!")
        exit()

    c = enc(pubkey, bytes_to_long(m.encode()))
    print("token to order yoshiking: ", c)

    c = [int(x) for x in input("your token: ")[1:-1].split(",")]
    if len(c) != len(set(c)):
        print("yoshiking: invalid!")
        exit()

    if any([x < 0 for x in c]):
        print("yoshiking: wow good unintended-solution!")
        exit()

    m = long_to_bytes(dec(privkey, c))
    if m == keyword.encode():
        print("yoshiking: hi!!!! flag!!!! here!!! wowowowowo~~~~~~")
        print(flag)
    else:
        print(m)
        print("yoshiking: ...?")


if __name__ == '__main__':
    main()
