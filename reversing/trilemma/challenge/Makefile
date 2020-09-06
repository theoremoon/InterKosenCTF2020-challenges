all:
	gcc -shared emperor.c -o libemperor.so -fPIC
	gcc -shared citizen.c -o libcitizen.so -fPIC
	gcc -shared slave.c -o libslave.so -fPIC
	mv lib*.so ../distfiles
	cp main.c ../distfiles
