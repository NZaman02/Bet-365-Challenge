from websocket import create_connection
import requests
import time

def read_csv(ws):
    ws.send("matchlivexy|")
    result = ws.recv()
    results = result.split("|")
    url = results[1]
    response = requests.get(url).content.decode()
    events = response.split("\n")
    print(len(events))
    for i in range(1, len(events)):
        event_type = events[i].split(",")[0]
        if (event_type == "goal"):
            send_goal(ws, events[i])
        if (event_type == "possession"):
            send_possetion(ws, events[i])
    ws.recv()
    ws.close()
        

def send_goal(ws, event):
    parts = event.split(',')
    message = "matchlivegoals|" + parts[0] + "|" + parts[1]
    ws.send(message)

def send_possetion(ws, event):
    print(event)
    parts = event.split(',')
    side = parts[1]
    coords = parts[2].split(":")
    x = int(coords[0])
    y = int(coords[1])
    possetion = "possession"
    if (side == "home"):
        if (x > (2/3)*400):
            possetion = "attack"
        if (x == 30 and (y == 120 or y == 60)):
            possetion = "goalkick"
        if (x == 400 and (y == 180 or y == 0)):
            possetion = "corner"
    if (side == "away"):
        if (x < (1/3)*400):
            possetion = "attack"
        if (x == 370 and (y == 120 or y == 60)):
            possetion = "goalkick"
        if (x == 0 and (y == 180 or y == 0)):
            possetion = "corner"

    message = "matchlivexy|" + possetion + "|" + side + "|" + parts[2]
    print(message)
    ws.send(message)

try:
    ws = create_connection("wss://service.codechallenge.co.uk/socket")
    print("Connected")
    ws.send('connect|{"teamName":"TeamPyPeople","password":"PythonPeople"}')
    print(ws.recv())
    read_csv(ws)


except Exception as ex:
    print("exception: ", format(ex))