import socket
import threading
import random
import re

print("SERVER_SYS")
# Server Configuration
HOST = '0.0.0.0'  # Listen on all available network interfaces
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
PORT= random.randint(1, 9999) #int(input("enter 4 digit port number for SERVER SIDE:"))
print("SERVER IP ",IP)
print("SECURE ID ",PORT)

# List to store connected clients
clients = []
user_names={}
def send_server_message():
    while True:
        message = input()
        if "remove_" in message:
            user_names[message[7:]][1].close()
            #socket.close()
        if message=="show_clients":
            print(f"members:{list(user_names.keys())}")
        else:
            broadcast("SERVER_SYS"+": " + message, None)
# Function to broadcast messages to all clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode())
            except:
                # Remove the client if unable to send a message
                remove_client(client)

# Function to remove a client
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

# Function to handle individual client connections
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                    print(message)  # Print the message to the server console
                    broadcast(message, client_socket)
            else:
                remove_client(client_socket)
        except:
            remove_client(client_socket)
            break

# Create and start the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
#print("Server is listening on port", PORT)

# Accept and handle client connections
while True:
    client_socket, client_address = server.accept()
    if client_socket not in clients:
        clients.append(client_socket)
        client_name = client_socket.recv(1024).decode()
        if client_name not in user_names:
            user_names[client_name]=[client_address[1],client_socket]
        else:
            remove_client(client_socket)
        # for user_name in user_names:
        #     if client_name not in user_name:
        #         user_names.append([client_address[1],client_name])
        #         print(f"Client {client_address} connected.")
        #     else:
        #         remove_client(client_socket)
    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
    
    server_message_thread = threading.Thread(target=send_server_message)
    server_message_thread.start()


