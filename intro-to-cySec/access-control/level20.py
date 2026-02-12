from pwn import *

## Variables
c = '/challenge/run'
p = process(c)  
d = p.recvuntil(b'}?\n').decode()
print(d)
levels = d.split('\n')[14:-8]
cat = d.split('ategories')[1].split('\n')[1:6]
q = d.split('\n')[-2]
#print(len(levels))
print(levels)
print(cat)
#print(len(cat))
try:
    while True:
        print(q)
        action = ''
        answer = 'yes'

        if q.find('read') == -1:
            action = 'write'
        else:
            action = 'read'

        SL = levels.index(q.split()[7])
        SC = q.split(action)[0].split('categories')[1][2:-2]

        OL = levels.index(q.split(action)[1].split()[4])
        OC = q.split(action)[1].split('categories')[1][2:-2]

        # action read
        if action == 'read':
            print('SL: '+str(SL))
            print('OL: '+str(OL))
            if SL > OL:
                answer = 'no'
                print(answer)
                p.sendline(answer.encode())
                q = p.recvline_startswith(b'Q ').decode()
                continue
            if len(SC.split(', ')) >= len(OC.split(', ')):
                for i in range(len(OC.split(', '))):
                    if SC.find(OC.split(', ')[i]) == -1:
                        answer = 'no'
                        break
            else:
                answer = 'no'

    # action write
        else:
            print('SL: '+str(SL))
            print('OL: '+str(OL))
            if SL < OL:
                answer = 'no'
                print(answer)
                p.sendline(answer.encode())
                q = p.recvline_startswith(b'Q ').decode()
                continue
            if len(SC.split(', ')) <= len(OC.split(', ')):
                for i in range(len(SC.split(', '))):
                    if OC.find(SC.split(', ')[i]) == -1:
                        answer = 'no'
                        break
            else:
                answer = 'no'

        print(answer)
        p.sendline(answer.encode())
        q = p.recvline_startswith(b'Q ').decode()
except:
    #print(error)
    print(p.recvall(timeout=1).decode())
