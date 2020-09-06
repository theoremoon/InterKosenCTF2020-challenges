FROM python:3.7-alpine

RUN apk --no-cache add socat

RUN apk add gcc
RUN apk add musl-dev
RUN apk add gmp-dev
RUN pip install pycryptodome

ADD challenge/server.py server.py
ADD challenge/secret.py secret.py

CMD socat TCP-L:13003,fork,reuseaddr EXEC:"python server.py"
