FROM python:3.7-alpine

RUN apk --no-cache add socat gcc g++ make libffi-dev openssl-dev
RUN pip3 install pycryptodome

ADD ./challenge/flag.py /flag.py
ADD ./challenge/server.py /server.py

CMD socat TCP-L:13001,fork,reuseaddr, EXEC:"python server.py"

