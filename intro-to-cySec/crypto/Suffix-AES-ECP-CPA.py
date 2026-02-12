from pwn import *

timeout=0.06
p = process('/challenge/run')
p.readlines(timeout=timeout)

chars = ''
for i in range(33, 126):
    chars+=chr(i)
print(chars+"\n=====================================\n")


length = 0
flag_part = ''
flag = ''

while length < 60:

    for c in chars:
        if flag_part == '':
            #data_block
            p.writeline(b'1')
            p.writeline(c.encode())
            result = p.readlines(timeout=timeout)
            data_block = str(result[0])[24:-1]
#            print("from flag='', data_block: "+data_block)

            #flag_block
            p.writeline(b'2')
            p.writeline(str(length+1).encode())
            result = p.readlines(timeout=timeout)
            flag_block = str(result[0])[26:-1]
 #           print("from flag='', flag_block: "+flag_block)

            if flag_block == data_block:
                print('Finish first loop')
                flag_part = c + flag_part

                print("found: "+flag_part)
                break
        else:
            flag = c + flag_part
            #data_block
            p.writeline(b'1')
            p.writeline(flag.encode())
            result = p.readlines(timeout=timeout)
            data_block = str(result[0])[24:-1]
   #         print("from for loop, data_block: "+data_block)

            #flag_block
            p.writeline(b'2')
            p.writeline(str(length+1).encode())
            result = p.readlines(timeout=timeout)
            flag_block = str(result[0])[26:-1]
    #        print("from for loop, flag_block: "+flag_block)

            if flag_block == data_block:
                flag_part = c + flag_part

                print("FOUND: "+flag_part)
                break

    length+=1

print("Here is you flag: "+flag_part)

