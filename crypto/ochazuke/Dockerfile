FROM sagemath/sagemath:latest

RUN sudo apt-get -y update --fix-missing
RUN sudo apt-get -y upgrade
RUN sudo apt-get install -y socat

RUN sudo apt-get install -y build-essential
RUN sudo apt-get install -y python3-dev
RUN sage -pip install pycryptodome

ADD challenge/chall.sage chall.sage
ADD challenge/secret.py secret.py

CMD ["socat", "TCP-L:13005,fork,reuseaddr", "EXEC:'sage chall.sage'"]