global _start


section .data
    digstr db "which is your choice? ["
    digstr2 db "]"
    invalidstr db "invalid choice",0xa
    congratzstr db "congratz. your choices are the flag",0xa
    goodbyestr db "try harder.",0xa
    buf db "{buf}"

section .bss
    inputbuf resb 2

section .text
_start:
    xor rbx,rbx
    xor r10,r10
f:
    inc r10
    mov rax, {target}
    cmp rax, rbx
    je congratz
    mov rax, {depth}
    cmp rax, r10
    jl goodbye

    mov rax, 1
    mov rdi, 1
    mov rsi, digstr
    mov rdx, 23
    syscall

    mov rax, 1
    mov rdi, 1
    lea rsi, [buf + rbx]
    mov rdx, 4
    syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, digstr2
    mov rdx, 1
    syscall

    mov rax, 0
    mov rdi, 0
    mov rsi, inputbuf
    mov rdx, 2
    syscall


    mov al, [inputbuf]
    xor rcx, rcx
    cmp al, [buf + rbx*1 + rcx]
    je valid
    inc rcx
    cmp al, [buf + rbx*1 + rcx]
    je valid
    inc rcx
    cmp al, [buf + rbx*1 + rcx]
    je valid
    inc rcx
    cmp al, [buf + rbx*1 + rcx]
    je valid

    mov rax, 1
    mov rdi, 1
    mov rsi, invalidstr
    mov rdx, 14
    syscall
    jmp e

valid:
    add rbx,rcx
    inc rbx
    shl rbx,2
    jmp f

congratz:
    mov rax, 1
    mov rdi, 1
    mov rsi, congratzstr
    mov rdx, 36
    syscall
    jmp e

goodbye:
    mov rax, 1
    mov rdi, 1
    mov rsi, goodbyestr
    mov rdx, 12
    syscall

e:
    mov rdi, 0
    mov rax, 60
    syscall
