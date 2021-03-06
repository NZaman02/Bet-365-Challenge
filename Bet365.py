from numpy import spacing
from websocket import create_connection
import requests
import time

def read_csv(ws):
    ws.send("matchlivetimes|")
    result = ws.recv()
    results = result.split("|")
    url = results[1]
    response = requests.get(url).content.decode()
    events = response.split("\n")
    curr_time = 0
    for i in range(1, len(events)):
        parts = events[i].split(",")
        event_type = parts[0]
        timer = parts[3]
        mins = int(timer.split(":")[0])
        sec = int(timer.split(":")[1])
        time.sleep(mins*60+sec - curr_time)
        curr_time = mins*60+sec
        if (event_type == "kickoff"):
            ws.send("matchlivetimes|kickoff||")
        if (event_type == "goal"):
            send_goal(ws, events[i])
        if (event_type == "possession"):
            send_possetion(ws, events[i])

    print("finnished")
    while True:
        print(ws.recv())
        

def send_goal(ws, event):
    parts = event.split(',')
    message = "matchlivegoals|" + parts[0] + "|" + parts[1] + "||"
    ws.send(message)
    print(message)

def send_possetion(ws, event):
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
    elif (side == "away"):
        if (x < (1/3)*400):
            possetion = "attack"
        if (x == 370 and (y == 120 or y == 60)):
            possetion = "goalkick"
        if (x == 0 and (y == 180 or y == 0)):
            possetion = "corner"

    message = "matchlivexy|" + possetion + "|" + side + "|" + parts[2] + "|"
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