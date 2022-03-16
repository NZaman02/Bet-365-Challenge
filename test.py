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
    response = requests.get(url).content.decode()
    events = response.split("\n")
    print(events)
    for i in range(1, len(events)):
        parts = events[i].split(',')
        message = "matchlivegoals|" + parts[0] + "|" + parts[1]
        print(type(message))
        print(message)
        ws.send(message)

except Exception as ex:
    print("exception: ", format(ex))
    