import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Client Configuration
HOST = "192.168.29.2"  # Replace with the IP address or hostname of the server
PORT = int(input("Enter 4 digit port number for SERVER SIDE:"))

# Function to receive and display messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                chat_area.config(state=tk.NORMAL)
                chat_area.insert(tk.END, message + "\n")
                chat_area.config(state=tk.DISABLED)
                chat_area.yview(tk.END)
        except:
            messagebox.showerror("Connection Error", "Connection to the server has been lost.")
            break

# Function to send messages to the server
def send_message(event=None):
    message = message_entry.get()
    message_entry.delete(0, tk.END)
    if message.lower() == 'exit':
        client.send('exit'.encode())
        client.close()
        root.quit()
    else:
        full_message = f"{user}: {message}"
        client.send(full_message.encode())
        display_sent_message(full_message)

# Function to display sent messages in the chat area
def display_sent_message(message):
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "You: " + message.split(":", 1)[1] + "\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)

# Create the main application window
root = tk.Tk()
root.title("Chat Application")

# Create the chat area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
chat_area.config(state=tk.DISABLED)
chat_area.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

# Create the message entry box
message_entry = tk.Entry(root, width=80)
message_entry.pack(padx=20, pady=5, fill=tk.X)
message_entry.bind("<Return>", send_message)

# Create the send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=20, pady=5)

print("------------Welcome To Chat-----------")
user = input("Enter username: ")

# Create a socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.send(user.encode())

# Start a thread to receive and display messages
receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.daemon = True
receive_thread.start()

# Start the Tkinter event loop
root.mainloop()
