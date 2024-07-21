import socket
import threading
import random

# Client Configuration
HOST = input("enter IP for SERVER SIDE:")  # Replace with the IP address or hostname of the server

PORT = int(input("enter 4 digit port number for SERVER SIDE:"))

# Function to receive and display messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
        except:
            print("Connection to the server has been lost.")
            break

# Create a socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Start a thread to receive and display messages
# receive_thread = threading.Thread(target=receive_messages, args=(client,))
# receive_thread.start()
print("------------Welcome To Chat-----------")
user=input("enter username:")
# Main loop to send messages to the server
receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()
client.send(user.encode())
while user:
    mess = input()
    message=user+":"+mess
    if mess.lower() == 'exit':
        client.send('exit'.encode())
        break
    client.send(message.encode())

# Close the client socket
client.close()
