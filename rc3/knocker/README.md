# knocker

We started off by connecting to the server, with the given port, and were greeted by the initial server message: "Welcome to the third annual short python challenge. You'll get one letter at a time and a new problem to solve each time. Left vague on purpose. You'll figure it out. Hit enter when you're ready...".
Pressing enter gave us a number and then after a short time it would time out and return the message "Better luck next time". We ran it a few times and got a few different results including: plain text numbers e.g. 'twenty four' and mathematical functions such as trunc() or ceil().
We decided to google 'python knocker' and discovered about port knocking (https://en.wikipedia.org/wiki/Port_knocking/). We looked back at the outputs and realised that the number it was giving us was the next port to knock: so we need to code a port knocker in python!

Using the 'socket' module we were able to open a connection to each port. We imported the functions from 'math' that we needed and then used the code, written by recursive, in this stackoverflow question, to parse the plain text numbers (https://stackoverflow.com/questions/493174/). The next port number was then taken care of by using eval() to evaluate any functions given to us.

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 7747
sock.connect(("18.216.59.235", port))
```
Not knowing how many characters were in the flag we ran the loop 50 times; creating a new socket object each time and adding it to a list for easy access.

Using socket.recv() returned the letter required for the flag as "b'<character>\n'" with <character> being a single character from the flag. We stored the flag character in a string variable and printed it out at the end.
This was where the first issue arose; the server was meant to return the flag character in one message and then send the next port number in the next message, however sometimes the server would send the flag character and the next port number in the same message and leave the next message blank. To overcome this I programmed in a check to see if the first message was more than 6 characters long, and then if it was, to use the second part of it as the str to evaluate.

```python
    if len(message) > 6:
        response = message[5:]
        dump = socketList[socketNumber].recv(1024)
    else:
        response = str(socketList[socketNumber].recv(1024))
```


We used a lot of replace() functions to strip the server messages of certain characters, whereas we should have used regex... but we were just aiming to get the flag, you can make it more efficient/prettier later! :)

```python
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
```

For an unknown reason the flag returned didn't have '}' at the end and it would just refuse the last connection, luckily we managed to get the important part of it though!

Flag was RC3-2017{i-am-the-0ne-wh0-kn0ckz}
