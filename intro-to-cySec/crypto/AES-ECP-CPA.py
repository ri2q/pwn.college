from pwn import *

## byte_list from 00 - ff

byte_list = []
c = '/challenge/run'
p = process(c)
p.readlines(timeout=0.3)

#for i in range(1, 256):
#    b = hex(i)[2:]
#    if len(b) < 2:
#        b = '0' + b
#    byte_list.append(b)
#print('Byte_list done'+b[0:3]+"....")

chars = ''
for i in range(33,126):
    chars+=chr(i)
print(chars+"\n=====================================\n")


index = 0
lenght = 1 # incread if we found one
flag = ''
flag_block = ''

p.writeline(b'1')
p.writeline(''.encode())
d_result = p.readlines(timeout=0.01)
    
blank_block = str(d_result[0])[24:-1]
print("Blank_Block: " +blank_block)

while blank_block != flag_block:

    for c in chars:
        p.writeline(b'1')
        p.writeline(c.encode())
        d_result = p.readlines(timeout=0.01)

        data_block = str(d_result[0])[24:-1]
        #print(data_block)

        p.writeline(b'2')
        p.writeline(str(index).encode())
        p.writeline(str(lenght).encode())
        f_result = p.readlines(timeout=0.01)

        flag_block = str(f_result[0])[33:-1]

        if flag_block == data_block:
            print("FOUND: " + c)
            flag =flag + c
            break
    index+=1
    print(flag_block)
    print(flag)

print("Here is you flag: "+flag)
