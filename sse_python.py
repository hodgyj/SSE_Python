import os
import json
import requests

sse_running = False
sse_address = ""
game_name = ""
game_friendly_name = ""

def json_post(url, data):
    r = requests.post(url, json=data)
    if r.status_code != 200:
        sse_running = False
        sse_status()

def register_game(icon_id):
    if sse_running:
        game_metadata = {
            "game": game_name,
            "game_display_name": game_friendly_name,
            "icon_color_id": icon_id
        }
        json_post(sse_address + "/game_metadata", game_metadata)

def remove_game():
    if sse_running:
        game_metadata = {
            "game": game_name
        }
        json_post(sse_address + "/remove_game", game_metadata)

def register_event(event, minimum, maximum, icon_id=0):
    if sse_running:
        event_data = {
            "game": game_name,
            "event": event,
            "min_value": minimum,
            "max_value": maximum,
            "icon_id": icon_id
        }
        json_post(sse_address + "/register_game_event", event_data)

def remove_event(event):
    if sse_running:
        event_data = {
            "game": game_name,
            "event": event
        }
        json_post(sse_address + "/remove_game_event", event_data)

def heartbeat():
    # Sends a heartbeat event to SSE3 so that colours stay there!
    if sse_running:
        sse_data = {
            "game": game_name
        }
        json_post(sse_address + "/game_heartbeat", sse_data)

def send_event(event, value):
            # This function sends a game event and value to SteelSeries
            # Engine 3 so that pretty colours are a thing
    if sse_running:
        sse_data = {
            "game": game_name,
            "event": event,
            "data": {
                "value": value
            }
        }
        json_post(sse_address + "/game_event", sse_data)

def sse_status():
    global sse_running
    global sse_address
    # coreProps file exists when SSE3 is running
    file_name = "C:/ProgramData/SteelSeries/SteelSeries Engine 3/coreProps.json"
    if os.path.isfile(file_name):
        sse_running = True
        with open(file_name) as sse_data_file:
            sse_data = json.load(sse_data_file)
        sse_address = "http://" + sse_data["address"]
    else:
        sse_running = False
    return sse_running
