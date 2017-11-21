#!/usr/bin/python3

import socket
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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 7747
sock.connect(("18.216.59.235", port))

socketList = []
socketList.append(sock)

for i in range(2):
    print(sock.recv(1024))

sock.send(b'\r')

answer = ''

for socketNumber in range(50):
    
    newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketList.append(newSocket)
    
    message = str(socketList[socketNumber].recv(1024))
    answer += message[2]

    if len(message) > 6:
        response = message[5:]
        dump = socketList[socketNumber].recv(1024)
    else:
        response = str(socketList[socketNumber].recv(1024))

    response = str(response.replace("b'",'',1))
    response = str(response[:-3])
    
    try:
        if 'and' in response:
            response = response.replace(',','')
            response = response.replace('-',' ')
            response = str(text2int(response))
    except:
        pass

    newPort = eval(str(response))
    socketList[sockNumber].close()
    print(answer)
    socketList[socketNumber+1].connect(('18.216.59.235', newPort))
