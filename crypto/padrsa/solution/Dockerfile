FROM sagemath/sagemath:latest

RUN sudo apt update -y && sudo apt upgrade -y
RUN sudo apt install -y socat build-essential python3-dev
RUN sage -pip install pycryptodome ptrlib

ADD solve.py solve.py

CMD sage solve.py
