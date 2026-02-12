#let's write a static boring response to our http clients

push rbp
mov r12, rax #to get the fd from accept return


mov rdi, r12
mov rsi, [rip+req_buf]
mov rdx, 1024
mov rax, 0
syscall


mov rdi, r12
lea rsi, [rip+resp]
mov rdx, 19
mov rax, 1
syscall

mov rdi, r12
mov rax, 3
syscall


resp:
.quad 0x485454502F312E30
.quad 0x20323030204F4B0D
.long 0x000A0D0A


.section .bss
req_buf: .skip 1024
