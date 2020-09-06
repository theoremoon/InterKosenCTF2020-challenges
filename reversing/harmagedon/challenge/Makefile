build:
	python3 gen.py
	nasm -f elf64 chall.asm -o chall.o
	ld chall.o -o harmagedon
	rm chall.o chall.asm
