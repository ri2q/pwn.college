.intel_syntax noprefix

.global _start

.section .text

_start:
# create a syscall socket
mov rdi, 2 #AF_INET opcode
mov rsi, 1 #SOCK_STREAM opcode
mov rdx, 0 #default tcp
mov rax, 41
syscall

mov r12, rax
#call bind to assign namespace for that socket
#bind(sockfd, struct sockaddr*, addr lenght)
mov rdi, r12
lea rsi, [rip+addr]
mov rdx, 16
mov rax, 49
syscall

#let's move to listen yabasha
#listen(sockfd, backlog)
mov rdi, r12
mov rsi, 0
mov rax, 50
syscall


#call Accept to answer to the caller and let him in 
mov rdi, r12
mov rsi, 0
mov rdx, 0
mov rax, 43
syscall

mov r12, rax
#read reqtest
mov rdi, r12
lea rsi, [rip+req_buf]
mov rdx, 1024
mov rax, 0
syscall

#write static boring 200 ok
mov rdi, r12
lea rsi, [rip+resp]
mov rdx, 19
mov rax, 1
syscall

#close
mov rdi, r12
mov rax, 3
syscall


#EXIT
mov rdi, 0
mov rax, 60
syscall



#sockaddr_in > have 4 properties > 'addr family, hton(port), ipv4, 16 pading bytes'
.section .data
addr:
.word 0x2 #AF_INET
.word 0x5000 #port 80 big endian
.long 0x0 #listen to any ip4
.quad 0x0

resp:
#quad 0x485454502F312E3120323030204F4B
.quad 0x302e312f50545448
.quad 0x0d4b4f2030303220
.long 0x0a0d0a


.section .bss
req_buf: .skip 1024

