import json
import socket

server_ip = "20.197.52.56"
server_port = 3001

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, server_port))

try:
    data = {
        "type": "detection",
        "data": "0"
    }
    data_json = json.dumps(data)
    client_socket.send(data_json.encode())
finally:
    client_socket.close()