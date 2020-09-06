FROM sagemath/sagemath:latest

RUN sudo apt update -y && sudo apt upgrade -y
RUN sudo apt install -y socat build-essential python3-dev
RUN sage -pip install pycryptodome ptrlib

ADD shattered-1.pdf shattered-1.pdf
ADD shattered-2.pdf shattered-2.pdf
ADD solver.sage solver.sage

CMD sage solver.sage
