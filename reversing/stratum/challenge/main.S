section .data
key: db "asdfghjklzxcvbnm"

section .text
global _start
;; zer0pts{h4v3_fun_w17h_7h3_ugly_bu7_u53ful_SIMD_1n57ruc710n5}
_start:
;; mprotect(text, 0x1000, RWX);
  call .@Popper1
  .@Popper1:
  mov dl, 7
  mov si, 0x1000
  mov al, 10
  pop rdi
  shr rdi, 12
  shl rdi, 12
  syscall

;; memset(rsp, 0, 0x40)
;; read(0, rsp, 0x40)
  xor eax, eax
  xor ecx, ecx
  mov rdi, rsp
  mov rsi, rdi
  mov cl, 0xc0
  mov dl, 0x40
  rep stosb
  xor edi, edi
  syscall

;; encode
  mov r8, rsi
  lea r9, [r8 + 0x40]
  xor ecx, ecx
  .@Lp1:
  movups xmm2, [r8 + rcx]
  lea eax, [ecx + 0x10]
  mov r10d, eax
  shr eax, 6
  shl eax, 6
  sub r10d, eax
  movups xmm3, [r8 + r10]
  movups xmm1, [key]
  pshufb xmm1, xmm2
  movups [r9 + 2 * rcx], xmm1

  call .@Popper2
  .@Popper2:
  pop rdi
  xor r12d, r12d
  mov rbp, r9
  .@Lp2:
  pextrb r11, xmm3, 0
  pextrb rax, xmm2, 0
  popcnt bx, ax
  shl bx, 4
  shl ax, 8
  lzcnt dx, ax
  or bx, dx
  xor bl, r11b
  mov [rbp + 2 * rcx + 0x10], bl
  inc r12d
  inc rbp
  cmp r12, 0x10
  shl r12b, 4
  shr r12b, 4
  mov [rdi + 13], r12b
  mov [rdi + 19], r12b
  jnz .@Lp2
  
  add ecx, 0x10
  cmp cl, 0x50
  jnz .@Lp1

;; write(1, rsp, 0x80)
  xor edi, edi
  add rsi, 0x40
  mov dl, 0x80
  inc edi
  mov eax, edi
  syscall

;; exit(0)
  xor edi, edi
  mov al, 60
  syscall
