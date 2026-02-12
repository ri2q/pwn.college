.intel_syntax noprefix
.global _start

.section .text
_start:
# initiate socket < 
mov rdi, 2
mov rsi, 1
mov rdx, 0
mov rax, 41
syscall

# mov p-fd to r12
mov r12, rax

# bind 
mov rdi, r12
lea rsi, [rip+sock_addr]
mov rdx, 16
mov rax, 49
syscall

# listen
mov rdi, r12
mov rsi,  0
mov rax, 50
syscall

# accept
mov rdi, r12
mov rsi, 0
mov rdx, 0
mov rax, 43
syscall

# mov c-fd into r13
mov r13, rax

ACCEPT:
# forking
mov rax, 57
syscall
cmp rax, 0
jne SKIP

# close c-fd? 
mov rdi, r12
mov rax, 3
syscall

sub rsp, 2064
# reading the request
mov rdi, r13
mov rsi, rsp
mov rdx, 1024
mov rax, 0
syscall

mov r10, 4
mov r14, 100 

CHECK:
mov bl, byte PTR [rsp+r10]
cmp bl, 0x20
je DONE

PARSE:
mov byte PTR [rsp+r14], bl
inc r14
inc r10
jmp CHECK

DONE:
mov byte PTR [rsp+r14], 0 #null terminator

# open the path 
lea rdi, [rsp+100]
mov rsi, 0
mov rax, 2
syscall

mov rbx, rax
# read that path
mov rdi, rbx
lea rsi, [rip+resp_data]
mov rdx, 1024
mov rax, 0
syscall

mov r10, rax

# close the opening path file 
mov rdi, rbx
mov rax, 3
syscall

# write the http status and version
mov rdi, r13
lea rsi, [rip+http_v]
mov rdx, 19
mov rax, 1
syscall

# write the resp
mov rdi, r13 # child socket fd
lea rsi, [rip+resp_data]
mov rdx, r10
mov rax, 1
syscall

mov rdi, 0
mov rax, 60
syscall

jmp ACCEPT

SKIP:
# close the socket
mov rdi, r13
mov rax, 3
syscall

# accept 'check on requests' 
mov rdi, r12
mov rsi, 0
mov rdx, 0
mov rax, 43 
syscall

#cmp rax, 1
jmp ACCEPT

add rsp, 200
.section .data
sock_addr:
.word 2 #AF
.word 0x5000
.long 0x0
.quad 0x0

http_v:
#485454502F312E3 020323030204F4B
.quad 0x302e312f50545448 
.quad 0x0d4b4f2030303220
.long 0x0a0d0a

# GET /Path HTTP/1.1
.section .bss
resp_data: .skip 1024

