import socket

# Change this to the server's IP address and port
server_ip = "20.197.52.56"
server_port = 3001

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, server_port))

while True:
    # Receive data from the server
    data = client_socket.recv(1024)

    # Decode the received bytes into a string
    received_data = data.decode("utf-8")

    print(f"Received data from server: {received_data}")
