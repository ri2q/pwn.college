.intel_syntax noprefix
.global _start

.section .text

_start:
# socket = l-fd
  mov rdi, 2
  mov rsi, 1
  mov rdx, 0
  mov rax, 41
  syscall

# l-fd = r10 
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

# accept = c-fd
  mov rdi, r10 
  mov rsi, 0
  mov rdx, 0
  mov rax, 43
  syscall

# c-fd =r14 
  mov r14, rax

# FORKING:
  FORKING:

# fork
  mov rax, 57
  syscall

# cmp on forking if not = 0 skip
  cmp rax, 0
  jne SKIP

# close l-fd
  mov rdi, r10 
  mov rax, 3
  syscall

# Start Processing incoming requests
## alocate space into stack `1500 b`
  sub rsp, 3000
    # 1500 > for the full request, 500 for the path, 1000 for the body
## read the request byte from `r14`
  mov rdi, r14 
  mov rsi, rsp
  mov rdx, 1500
  mov rax, 0
  syscall

## save req len = `r12`
  mov r12, rax

## check on first byte if G or P
  cmp byte ptr [rsp], 'G'
  je GET
  cmp byte ptr [rsp], 'P'
  je POST

## GET
  GET:
## if it's GET
### Extracting the Path using rcx, rbx
  mov rcx, 4
  mov rbx, 1500

  CHECK_G:
  mov dl, byte ptr [rsp+rcx]
  cmp dl, 0x20
  je DONE_G
  
  mov byte ptr [rsp+rbx], dl
  inc rcx
  inc rbx
  jmp CHECK_G

  DONE_G:
  mov byte ptr [rsp+rbx], 0

### open the path with O_RONLY = `rbx`
  lea rdi, [rsp+1500]
  mov rsi, 0
  mov rax, 2
  syscall

  mov rbx, rax

### read the Open file 'rbx'
  mov rdi, rbx
  lea rsi, [rsp+2000]
  mov rdx, 1000
  mov rax, 0
  syscall

### save the lengh into `r12`
  mov r12, rax

### close opening file 'rbx'
  mov rdi, rbx
  mov rax, 3
  syscall

### write the http status and the version `r14`
  mov rdi, r14
  lea rsi, [rip+http_v_s]
  mov rdx, 19
  mov rax, 1
  syscall

### write the content of the file to the response `r14`
  mov rdi, r14
  lea rsi, [rsp+2000]
  mov rdx, r12
  mov rax, 1
  syscall

### Exit
  mov rdi, 0
  mov rax, 60
  syscall

### Jmp to forking again to skip POST process
  jmp FORKING

## POST:
  POST:
## if it's POST
### Extracting the Path using rcx, rbx
  mov rcx, 5
  mov rbx, 1500

  CHECK_p:
  mov dl, byte ptr [rsp+rcx]
  cmp dl, 0x20
  je DONE_p
  
  mov byte ptr [rsp+rbx], dl
  inc rcx
  inc rbx
  jmp CHECK_p

  DONE_p:
  mov byte ptr [rsp+rbx], 0

### open the path with O_WRONLY + O_CREAT + 0777 perm = `rbx`
  lea rdi, [rsp+1500]
  mov rsi, 65
  mov rdx, 0777
  mov rax, 2
  syscall

  mov rbx, rax

### Parse the body
  xor r15, r15
  EXTRACT_END_HEADER:
  cmp dword ptr [rsp+r15], 0x0a0d0a0d
  je SAVE
  inc r15
  jmp EXTRACT_END_HEADER
  
  SAVE:
  lea rcx, [rsp+r15+4]
  sub r12, r15
  sub r12, 4

### write the body to the Open file `rbx`
  mov rdi, rbx
  mov rsi, rcx
  mov rdx, r12
  mov rax, 1
  syscall

### close open file `rbx`
  mov rdi, rbx
  mov rax, 3
  syscall

### write http status and version to `r14`
  mov rdi,r14 
  lea rsi, [rip+http_v_s]
  mov rdx, 19
  mov rax, 1
  syscall

### Exit
  mov rdi, 0
  mov rax, 60
  syscall

# Jmp to Forking
jmp FORKING

# skip
SKIP:

# close c-fd `r14`
  mov rdi, r14 
  mov rax, 3
  syscall

# accept check on `r10 fd`
  mov rdi, r10 
  mov rsi, 0
  mov rdx, 0
  mov rax, 43
  syscall

# jmp fork
jmp FORKING

# data
  add rsp, 3000
  .section .data

  sock_addr:
  .word 2 #AF
  .word 0x5000
  .long 0x0
  .quad 0x0

  http_v_s:
  #485454502F312E3 020323030204F4B
  .quad 0x302e312f50545448 
  .quad 0x0d4b4f2030303220
  .long 0x0a0d0a






