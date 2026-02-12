import requests
import base64


n = 51

flag = ''
chars = ''
url = 'http://challenge.localhost:80/'

r = requests.get(url)
print(r)

def reset():
    reset = requests.post(url+'reset')

def cipherText():
    resp = requests.get(url)
    ct = base64.b64decode(resp.text.split()[-2][16:-6]).hex()
    return ct

def sendPayload(body):
    resp = requests.post(url, body)


for i in range(33,126):
    chars+=chr(i)

print('Chars Done.')


while n > 3:
    x='x'*n
    for c in chars:
        reset()

        # handling brute_block
        x_brute = x+'|pwn.college'+flag+c
        payload = x_brute+x
     #   print("payload: "+payload)
        body = {'content':payload}
      #  print(body)
        sendPayload(body)
        ct = cipherText()
        brute_block = ct[:128]
       # print("brute_block: "+brute_block)

        #handling flag_block
        flag_block = ct[128:256]
        #print('flag_block: ', flag_block)

        if flag_block == brute_block:
            print('FOUND: '+c)
            flag+=c
            break

    print('pwn.college'+flag)
    n-=1

print('Done: pwn.college'+flag)




