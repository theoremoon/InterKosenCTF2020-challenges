# assert the flag exists
try:
    flag = open("flag.txt", "rb")
except:
    print("[-] Report this bug to the admin.")

# help yourself :)
path = input("> ")
if 'flag.txt' in path:
    print("[-] Nope :(")
elif 'self' in path:
    print("[-] No more procfs trick :(")
elif 'dev' in path:
    print("[-] Don't touch it :(")
else:
    try:
        f = open(path, "rb")
        print(f.read(0x100))
    except:
        print("[-] Error")
