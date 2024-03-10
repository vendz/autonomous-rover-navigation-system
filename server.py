import socket
import threading

# Change this to the server's IP address and port
server_ip = "127.0.0.1"
server_port = 3001

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((server_ip, server_port))

# Listen for incoming connections
server_socket.listen()

print(f"Server listening on {server_ip}:{server_port}")

# List to keep track of connected clients
clients = []


def handle_client(client_socket):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break  # Break the loop if no data is received

            # Broadcast the received data to all connected clients
            for other_client in clients:
                if other_client != client_socket:
                    try:
                        other_client.send(data)
                    except Exception as e:
                        # Remove disconnected clients
                        clients.remove(other_client)
                        print(f"Client {other_client} disconnected")

        except Exception as e:
            print(f"Error handling client: {e}")
            break


while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()

    # Add the new client to the list
    clients.append(client_socket)
    print(f"Connected to client {client_address}")

    # Create a new thread to handle the client
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
