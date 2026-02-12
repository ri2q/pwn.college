import requests

chars=''

for i in range(33,126):
    chars+=chr(i)

print("Chars Done: "+chars)



resp = requests.get("http://challenge.localhost:80/?query='';--")

blank_block = resp.text.split()[-2][20:-6]
print("blank_block: "+blank_block)

flag_block = ''
index = 1
flag = ''

while blank_block != flag_block:

    for c in chars:
        resp = requests.get("http://challenge.localhost:80/?query='"+c+"';--")
        data_block = resp.text.split()[-2][20:-6]
 #       print(data_block)
        
        resp = requests.get("http://challenge.localhost:80/?query=substr(flag,"+str(index)+",1) from secrets;--")
        flag_block =  resp.text.split()[-2][20:-6]
#        print(flag_block)

        if data_block == flag_block:
            print(flag_block)
            print("FOUND: "+c)
            flag+=c
            break

    print(flag)
    index+=1


print('Here is your flag: '+flag)
