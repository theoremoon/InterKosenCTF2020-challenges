all:
	gcc -Wl,-z,lazy,-z,relro main.c -o chall -no-pie -fstack-protector
	mv chall ../distfiles
	cp main.c ../distfiles
