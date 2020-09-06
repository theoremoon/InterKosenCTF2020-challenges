FROM python:3.7-alpine

RUN adduser -D app
RUN pip install Flask
RUN apk add m4
RUN apk add graphviz

ADD challenge/init.sh /etc/init.sh
RUN chmod 555 /etc/init.sh
RUN chmod 1733 /tmp /var/tmp /dev/shm

WORKDIR /home/app
ADD challenge/flag.txt             flag_foxtrot.txt
ADD challenge/app.py               app.py
ADD challenge/dotmerger.py         dotmerger.py
ADD challenge/templates/index.html templates/index.html

RUN chown -R root:app /home/app
RUN chmod 440 /home/app/flag_foxtrot.txt
RUN chmod 550 /home/app/templates
RUN chmod 440 /home/app/templates/index.html
RUN chmod 550 /home/app/app.py

USER app
