FROM python:3.7-alpine

RUN apk --no-cache add socat
RUN adduser -D ctf

ADD challenge/server.py /home/ctf/server.py
ADD challenge/flag.txt  /home/ctf/flag.txt
RUN chmod 500 /home/ctf/server.py
RUN chmod 400 /home/ctf/flag.txt
RUN chown ctf:root /home/ctf -R

USER ctf
WORKDIR /home/ctf
CMD socat TCP-L:9712,fork,reuseaddr EXEC:"python3 ./server.py",stderr
