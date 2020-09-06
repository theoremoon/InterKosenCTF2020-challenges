flag = b'KosenCTF{d0nt_l3t_th4t_f00l_u}\0'

answer = []
for i in range(len(flag) - 1):
    answer.append(flag[i] ^ flag[i+1] ^ i ^ 0xff)
print(answer)
