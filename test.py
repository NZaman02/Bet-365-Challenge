import json
from websocket import create_connection

try:
    ws = create_connection("wss://service.codechallenge.co.uk/socket")
    ws.send('connect|{"teamName":"TeamPyPeople","password":"PythonPeople"}')
except Exception as ex:
    print("exception: ", format(ex))
    