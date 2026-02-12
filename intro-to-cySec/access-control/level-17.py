from pwn import * 

## Variables

c = '/challenge/run'
p = process(c)
levels = ['UC', 'C', 'S', 'TS']
cat = ['NUC', 'ACE', 'UFO', 'NATO']
try:
while True:    
    #lines = p.readlines(timeout=0.07)
    #print("lines: ",lines.decode())
    #l = lines.decode().split("\n")[-2]

    l = p.recvline_startswith(b'Q ').decode()
    print(l)
    action = ''
    answer = 'yes'

    if l.find('read') == -1:
        action = 'write'
    else:
        action = 'read'
    SL = levels.index(l.split()[7])
    SC = str(l.split(action)[0]).split('categories')[1][2:-2]

    OL = levels.index(str(l.split(action)[1]).split()[4])
    OC = str(l.split(action)[1]).split('categories')[1][2:-3]

    # action read
    if action == 'read':
        if SL < OL:
	        answer = 'no'
        elif len(SC.split(', ')) >= len(OC.split(', ')):
            for i in range(len(OC.split(', '))):	 
                if SC.find(OC.split(', ')[i]) == -1:
                    answer = 'no'
                    break
        else:
            answer = 'no'

# action write
    else:
        if SL > OL:
            answer = 'no'
        elif len(SC.split(', ')) <= len(OC.split(', ')):
            for i in range(len(SC.split(', '))):
                if OC.find(SC.split(', ')[i]) == -1:
                    answer = 'no'
                    break
        else:
            answer = 'no'

    print(answer)
    p.sendline(answer.encode())


