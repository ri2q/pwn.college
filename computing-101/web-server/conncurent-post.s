.intel_syntax noprefix
.global _start

.section .text

_start:
# socket return p-fd
mov rdi, 2
mov rsi, 1
mov rdx, 0
mov rax, 41
syscall

# mov p-fd > r10
mov r10, rax

# bind
mov rdi, r10
lea rsi, [rip+sock_addr]
mov rdx, 16
mov rax, 49
syscall

# listen
mov rdi, r10
mov rsi, 0
mov rax, 50
syscall

# accept return c-fd
mov rdi, r10
mov rsi, 0
mov rdx, 0
mov rax, 43
syscall

# mov c-fd > r14
mov r14, rax

# FORKING:
FORKING:
# fork
mov rax, 57
syscall
  
  ## cmp on return if not child jmp SKIP
                cmp rax, 0
                jne SKIP

  ## close r10
                mov rdi, r10
                mov rax, 3
                syscall

  ## allocate buf for post request in stack `1000 byte`
                sub rsp, 1200

  ## read the post request to `500 byte`
                mov rdi, r14
                mov rsi, rsp
                mov rdx, 500
                mov rax, 0
                syscall
  
  ## saving request lenght to r12
                mov r12, rax

  ## parse the req path from 'POST /path ....'
                mov rcx, 5
                mov rbx, 500 # to save path into this location 

                CHECK:
                mov dl, byte ptr [rsp+rcx] 
                cmp dl, 0x20
                je DONE
                mov byte ptr [rsp+rbx], dl
                inc rcx
                inc rbx
                jmp CHECK

                DONE:
                mov byte ptr [rsp+rbx], 0 # 0 null terminator

  ## parse the body usig request length
                mov rbx, 800
                xor r13, r13

                x0A_CHECK:
                mov dl, byte ptr [rsp+r12]
                cmp dl, 0x0a
                je x0A_DONE

                inc r13
                mov byte ptr [rsp+rbx], dl
                dec r12
                dec rbx
                jmp x0A_CHECK

                x0A_DONE:
                mov r11, rbx

  ## open the path
                lea rdi, [rsp+500]
                mov rsi, 65
                mov rdx, 0777
                mov rax, 2
                syscall

        ## save o-fd to rbx
                mov rbx, rax

  ## write the body to path
                mov rdi, rbx
                lea rsi, [rsp+r11]
                mov rdx, r13
                mov rax, 1
                syscall

  ## close the o_fd
                mov rdi, rbx
                mov rax, 3
                syscall

  ## write http version and status 'HTTP/1.0 200 ok\r\n\r\n' 
        mov rdi, r14
        lea rsi, [rip+http_v]
        mov rdx, 19
        mov rax, 1
        syscall
  ## EXIT 
        mov rdi, 0
        mov rax, 60
        syscall

# jmp FORKING
jmp FORKING

# SKIP:
SKIP:
# close r14
mov rdi, r14
mov rax, 3
syscall

# accept 'Checking on incoming request'
mov rdi, r10
mov rsi, 0
mov rdx, 0
mov rax, 43
syscall

# jmp FORKING
jmp FORKING

# Clean the stack
add rsp, 1200
.section .data
sock_addr:
.word 2
.word 0x5000
.long 0x0
.quad 0x0

http_v:
#485454502F312E3 020323030204F4B
.quad 0x302e312f50545448 
.quad 0x0d4b4f2030303220
.long 0x0a0d0a

