FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install openssh-server

RUN groupadd -r admin && useradd -r -g admin admin
RUN groupadd pwn && useradd -g pwn pwn
RUN printf "/bin/bash\n" | chsh pwn
RUN printf "guest\nguest\n" | passwd pwn

RUN mkdir /var/run/sshd
RUN rm /etc/update-motd.d/*
RUN rm /etc/legal

RUN chmod 1733 /tmp /var/tmp /dev/shm

WORKDIR /home/pwn
RUN printf "trap 'kill -9 \$PPID' INT\nmesg n\n/home/pwn/pash\nkill -9 \$PPID\n" >> .bash_profile
ADD challenge/flag.txt flag.txt
ADD challenge/pash.rs  pash.rs
ADD challenge/pash     pash
RUN chmod 440 flag.txt
RUN chmod 555 pash
RUN chown -R root:pwn /home/pwn
RUN chmod 550 /home/pwn

RUN chown root:admin /home/pwn/flag.txt
RUN chown root:admin /home/pwn/pash
RUN chmod g+s        /home/pwn/pash
