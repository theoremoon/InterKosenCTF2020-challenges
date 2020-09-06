#FLAG=zer0pts{h4v3_fun_w17h_7h3_ugly_bu7_u53ful_SIMD_1n57ruc710n5}
FLAG=KosenCTF{h4v3_fun_w17h_7h3_ugly_bu7_u53ful_SIMD_1n57ruc710n5}

all:
	nasm main.S -o main.o -fELF64
	ld main.o -o chall
	rm main.o
	strip --strip-all chall
	mv chall ../distfiles
	cd ../distfiles; FLAG="$(FLAG)" ./chall.sh
