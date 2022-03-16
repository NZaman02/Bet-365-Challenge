from websocket import create_connection
import requests

try:
    ws = create_connection("wss://service.codechallenge.co.uk/socket")
    print("Connected")
    ws.send('connect|{"teamName":"TeamPyPeople","password":"PythonPeople"}')
    print(ws.recv())
    ws.send('matchlivegoals|')
    result = ws.recv()
    results = result.split("|")
    url = results[1]
    print(url)
    response = requests.get(url)
    print (response.status_code)
    print (response.content)
except Exception as ex:
    print("exception: ", format(ex))
    