#!/usr/bin/python3

import socket
import re
from math import floor, trunc, ceil

def text2int(textnum, numwords={}):
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current

sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port1 = 7747
sock1.connect(("18.216.59.235", port1))

sockList = []
sockList.append(sock1)

for newPort in range(1,50):
    newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockList.append(newSocket)

for i in range(1,3):
    print(sock1.recv(1024))

sock1.send(b'\r')

regEx = "b'.n(.*).n'"

answer = ''

for sockNumber in range(50):


    message = str(sockList[sockNumber].recv(1024))
    #print(message)
    #print(sockList[sockNumber].recv(1024))
    answer += message[2]

    if len(message) > 6:
        x1 = message[5:]
        dump = sockList[sockNumber].recv(1024)
    else:
        x1 = str(sockList[sockNumber].recv(1024))
    #print('x1 is currently: ',  x1)
    '''m1 = re.search(regEx, x1)
    i1 = m1.group(1)
    '''
    #print(x1)
    x1 = str(x1.replace("b'",'',1))
    '''if sockNumber == 4:
        x1 = x1[4:-3]
    else:'''
    x1 = str(x1[:-3])
    #print(x1)
    i1 = str(x1)
    try:
        if 'and' in i1:
            i1 = i1.replace(',','')
            i1 = i1.replace('-',' ')
            i1 = str(text2int(i1))
            #print('converted')
    except:
        print('fail')


    port2 = eval(str(i1))
    #print(port2)
    sockList[sockNumber].close()
    print(answer)
    sockList[sockNumber+1].connect(('18.216.59.235', port2))
