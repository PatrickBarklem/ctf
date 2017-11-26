from pwn import *
import re

r = remote("neverending.tuctf.com", 12345)
r.recv()

for x in range (50):
    r.send('a'+"\n")
    msg = r.recv()

    cmpregex = 'is (.)'

    compare = re.search(cmpregex, msg)
    compare = compare.group(1)

    msgregex = ('is (.+) decrypted')
    result = re.search(msgregex, msg)
    result = result.group(1)

    answer = ''
    difference = ord('a')-ord(compare)

    for i in range(len(result)):

        if ord(result[i])+difference > 126:
            answer += chr(32+(ord(result[i])+difference)-127)
        elif ord(result[i])+difference < 32:
            answer += chr((ord(result[i])+difference)+95)
        else:
            answer += chr(ord(result[i])+difference)
    r.send(answer+"\n")
    if x == 49:
        victory = r.recv()
        vicReg = '(TUCTF\{.+\})'
        victory = re.search(vicReg,victory)
        print victory.group(1)
    else:
        r.recv()
