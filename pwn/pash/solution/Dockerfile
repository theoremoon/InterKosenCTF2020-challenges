FROM python:3.7-alpine

RUN apk --no-cache add gcc
RUN apk add musl-dev
RUN apk add gmp-dev
RUN pip install ptrlib
RUN apk add expect
RUN apk add openssh

WORKDIR /solution
ADD solve.py .

CMD python solve.py
