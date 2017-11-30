from pwn import *
import re

r = remote("neverending.tuctf.com", 12345)
r.recv()

for x in range (50):
    r.send('a'+"\n")
    msg = r.recv()

    compare = re.search('is (.)', msg)
    compare = compare.group(1)

    result = re.search('is (.+) decrypted', msg)
    result = result.group(1)

    answer = ''
    difference = ord('a')-ord(compare)

    for i in range(len(result)):

        if ord(result[i])+difference > 126:
            answer += chr((ord(result[i])+difference)-95)
        elif ord(result[i])+difference < 32:
            answer += chr((ord(result[i])+difference)+95)
        else:
            answer += chr(ord(result[i])+difference)
    r.send(answer+"\n")
    if x == 49:
        victory = r.recv()
        victory = re.search('(TUCTF\{.+\})',victory)
        print victory.group(1)
    else:
        r.recv()
