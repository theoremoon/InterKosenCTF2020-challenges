FROM python:3.7-alpine

RUN apk --no-cache add socat

RUN apk add gcc
RUN apk add musl-dev
RUN apk add gmp-dev
RUN pip install pycryptodome ptrlib

ADD solve.py solve.py
CMD python solve.py
