import socket
import requests
import flexpolyline as fp
import math

import serial
import time

# arduino_port = "COM6"
# baud = 9600

# ser = serial.Serial(arduino_port, baud)
# print("Connected to Arduino port:" + arduino_port)
# time.sleep(2)

# Change this to the server's IP address and port
server_ip = "20.197.52.56"
server_port = 3001
api_key = "RrMCCYQSGxDslgEpPoLctIDUiMV1LLFElGl9dfiMeaw"
current_lat = None
current_long = None

destination_coordinates = [-1, -1]
start_coordinates = [-1, -1]
offsets = []
steps = None
decoded_polyLine = []

i = 0
j = 0
threshold = 0.02

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, server_port))


def get_route(start_coords, destination_coords):
    base_url = "https://router.hereapi.com/v8/routes"

    params = {
        "apiKey": api_key,
        "transportMode": "car",
        "origin": f"{start_coords[0]},{start_coords[1]}",
        "destination": f"{destination_coords[0]},{destination_coords[1]}",
        "return": "polyline,turnbyturnactions",
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        route_data = response.json()
        return route_data
    else:
        print(f"Error: {response.status_code}")
        return None


def initialize():
    # destination_coordinates[0] = input("Enter the latitude of the destination: ")
    # destination_coordinates[1] = input("Enter the longitudeof the destination: ")
    destination_coordinates[0] = 12.970819692361477
    destination_coordinates[1] = 79.15952504976268
    start_coordinates[0] = current_lat
    start_coordinates[1] = current_long
    get_directions(start_coordinates, destination_coordinates)


def get_directions(start_coordinates, destination_coordinates):
    global steps
    global decoded_polyLine
    route_data = get_route(start_coordinates, destination_coordinates)
    if route_data:
        # Extract and print step-by-step directions
        steps = route_data["routes"][0]["sections"][0]["turnByTurnActions"]
        print(steps)
        polyLine = route_data["routes"][0]["sections"][0]["polyline"]
        decoded_polyLine = fp.decode(polyLine)
        for step in steps:
            offsets.append(step["offset"])
    else:
        print("Failed to retrieve routing directions.")
    print("\n")


def navigate_user(current_lat, current_long):
    global j, i
    global steps
    global decoded_polyLine
    R = 6371  # Earth radius in kilometers

    # Convert latitude and longitude from degrees to radians
    step = steps[j]
    lat1, lon1, lat2, lon2 = map(
        math.radians,
        [
            float(current_lat),
            float(current_long),
            float(decoded_polyLine[step["offset"]][0]),
            float(decoded_polyLine[step["offset"]][1]),
        ],
    )

    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    if distance <= threshold:

        if step["action"] == "turn":
            print(
                f"{step['action']} {step['direction']} at {decoded_polyLine[step['offset']]}"
            )
            # ser.write(bytes(step["direction"], "utf-8"))
        elif step["action"] == "arrive":
            print("Arrived at destination")
            # ser.write(bytes("stop", "utf-8"))
            exit(0)
        else:
            print(f"{step['action']} at {decoded_polyLine[step['offset']]}")
            # ser.write(bytes("forward", "utf-8"))
        i += 1
        j += 1


while True:
    # Receive data from the server
    data = client_socket.recv(1024)

    received_data = data.decode("utf-8")

    current_coords = received_data.split(",")
    try:
        current_lat = float(current_coords[0])
        current_long = float(current_coords[1])
    except:
        current_coords = data.split(",")
        current_lat = float(current_coords[0])
        temp = current_coords[1].split(".")
        temp1 = float(temp[0].strip() + "." + temp[1][:-2])

    if steps is None:
        initialize()
    navigate_user(current_lat, current_long)
