all:
	gcc -Wl,-z,lazy,-z,relro main.c -o chall -fstack-protector -no-pie -O2
	mv chall ../files
	cp main.c ../files
	cp type.h ../files
	cp /lib/x86_64-linux-gnu/libc-2.27.so ../files
