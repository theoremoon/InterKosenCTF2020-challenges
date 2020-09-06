all:
	gcc -Wl,-z,lazy,-z,relro main.c -o chall -fno-stack-protector -no-pie	
	mv ./chall ../distfiles
	cp ./main.c ../distfiles
