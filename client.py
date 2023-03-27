import socket
import threading

# define the server's IP address and port
IP_ADDRESS = '127.0.0.1'
PORT = 12345

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
client_socket.connect((IP_ADDRESS, PORT))

def receive_messages():
    while True:
        # receive messages from the server
        message = client_socket.recv(1024).decode()
        print(message)

# start a new thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    # get user input
    user_input = input()

    if user_input == "list":
        # request a list of all connected clients from the server
        client_socket.send(b"list")

    elif user_input == "exit":
        # exit the chat room
        client_socket.send(b"exit")
        break

    else:
        # send the user's message to the server
        client_socket.send(user_input.encode())
