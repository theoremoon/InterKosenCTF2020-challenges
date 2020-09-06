all:
	musl-gcc main.c -o chall -Os -static -masm=intel
	python modify.py
	python corrupt.py
