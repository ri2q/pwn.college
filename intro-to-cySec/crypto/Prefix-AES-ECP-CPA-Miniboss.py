from pwn import *
timeout=0.08
p = process('/challenge/run')
p.readlines(timeout=timeout)

chars=''
for i in range(33, 126):
    chars+=chr(i)
print('chars done...')


flag=''
n=52

while n > 4:

    x = ('78'*n).encode()

    for c in chars:
        payload = x+(('pwn.college'+flag+c).encode().hex()).encode()
        #print(payload)
       ## handling the flag_block
        p.writeline(x)
        res = p.readlines(timeout=timeout)
        flag_block = str(res[0])[14:142]
        #print("flag_block: "+flag_block)
        ## handling the brute_block
        #print("\n================================================\n")
        p.writeline(payload)
        res = p.readlines(timeout=timeout)
        brute_block = str(res[0])[14:142]
        #print("brute_block: "+brute_block)

        if flag_block == brute_block:
            print("FOUND: "+c)
            print("payload+c: "+str(bytes.fromhex(payload.decode())))
            flag += c
            n-=1
            break

    print("pwn.college"+flag+"..")



print("Done: pwn.college"+flag)
