import json
from websocket import create_connection

try:
    ws = create_connection("wss://service.codechallenge.co.uk/socket")
    ws.send('connect|{"teamName":"TeamPyPeople","password":"PythonPeople"}')
    ws.send('echo|HelloWorld')
    while True:
        result = ws.recv()
        print(result)
except Exception as ex:
    print("exception: ", format(ex))
    