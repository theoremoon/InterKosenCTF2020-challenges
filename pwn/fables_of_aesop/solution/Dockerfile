FROM python:3.7-alpine

RUN apk --no-cache add gcc
RUN apk add musl-dev
RUN apk add gmp-dev
RUN pip install ptrlib

WORKDIR /distfiles
ADD chall .
ADD libc-2.23.so .
WORKDIR /solution
ADD solve.py .

CMD python solve.py
