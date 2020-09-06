FROM python:3.7-alpine

RUN apk --no-cache add socat

RUN apk add gcc
RUN apk add musl-dev
RUN apk add gmp-dev
RUN pip install pycryptodome

ADD challenge/chall.py chall.py
ADD challenge/flag.txt flag.txt

CMD socat TCP-L:10002,fork,reuseaddr EXEC:"python3 ./chall.py",stderr