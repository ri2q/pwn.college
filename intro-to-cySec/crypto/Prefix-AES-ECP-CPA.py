from pwn import *


blocks = []
timeout=0.05
p = process('/challenge/run')
p.readlines(timeout=timeout)


chars=''
for i in range(33, 126):
    chars+=chr(i)
print('chars done...')

data = 'f5d1bc079b4e4b26ddcfc52f928f0978f5d1bc079b4e4b26ddcfc52f928f0978f5d1bc079b4e4b26ddcfc52f928f0978c97ca5be325a86d30ae53bc551c8e9cdf25ed9653df361fbcfaa028a6bcbd1fb4aad54795fb2b788cce10245d88cdd18a30b6b55b70f5f189ecf73b28ded961821ed05eb251027f4961489a97ebdd085'

def blocks_split(data):
    blocks = []
    f = 0
    t = 32
    while f < len(data):
        block = data[f:t]
        blocks.append(block)
        f+=32
        t+=32

    return blocks

print("blocks done: "+blocks_split(data)[0])

## first 10 blocks
for i in range(10):
    p.writeline(b'2')
    p.writeline(b'')
    p.readlines(timeout=timeout)

print("finish realesing first 10 shit..")

n = 52

flag = ''
flag_part = ''

while n > 4:

    x = 'x'*n
    payload = 'x'*n+'pwn.college'+flag_part

    for c in chars:
        ## handling the flag_block
        p.writeline(b'2')
        p.writeline(x.encode())
        res = p.readlines(timeout=timeout)
        data = str(res[0])[24:-1]
        blocks = blocks_split(data)
        #print("a from flag: "+ blocks[0])
        flag_block = blocks[3]
        #print(blocks)
        #print('flag_block: '+flag_block)
        
        ## handling the brute_block
       #print("================================================")
        p.writeline(b'1')
        p.writeline((payload+c).encode())
        res = p.readlines(timeout=timeout)
        brute_block = str(res[0])[120:-1]
        #print("brute_block: "+brute_block)
        #print('a from brute: '+str(res[0])[24:-32])
        if flag_block == brute_block:
            print("FOUND: "+c)
            print("payload+c: "+payload+c)
            flag_part += c
            n-=1
            break

    print("pwn.college"+flag_part+"....")



print("Done: pwn.college"+flag_part)

