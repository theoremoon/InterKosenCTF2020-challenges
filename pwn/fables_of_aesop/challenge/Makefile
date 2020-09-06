all:
	gcc -Wl,-z,now,-z,relro main.c -o chall -fstack-protector-all -pie -Wno-implicit-function-declaration
	strip --strip-all ./chall
	mv chall ../distfiles
	cp banner.txt ../distfiles
	cp main.c ../distfiles
