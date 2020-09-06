FROM python:3.7-alpine

RUN apk --no-cache add gcc musl-dev gmp-dev
RUN pip install pycryptodome ptrlib

ADD solve.py solve.py
CMD python solve.py
