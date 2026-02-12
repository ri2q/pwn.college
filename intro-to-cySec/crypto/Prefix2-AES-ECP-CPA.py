from pwn import *
blocks = []
timeout=0.11
p = process('/challenge/run')
p.readlines(timeout=timeout)


chars=''
for i in range(33, 126):
    chars+=chr(i)
print('chars done...')

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

print("blocks done ")

## first 10 blocks
#for i in range(10):
   # p.writeline(b'2')
  #  p.writeline(b'')
 #   p.readlines(timeout=timeout)

#print("finish realesing first 10 shit..")

n = 52
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
       # print('Cipher flag+payload: '+data)
        blocks = blocks_split(data)
       # print("a from flag: "+ blocks[0])
        flag_block = blocks[3]
        #print(blocks)
        #print('flag_block: '+flag_block)

        ## handling the brute_block
        #print("================================================")
        p.writeline(b'1')
        p.writeline((payload+c).encode())
        res = p.readlines(timeout=timeout)
        brute_block = str(res[0])[-65:-33]
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
