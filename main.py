import socket
import threading

# define the server's IP address and port
IP_ADDRESS = '127.0.0.1'
PORT = 12345

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket object to the IP address and port
server_socket.bind((IP_ADDRESS, PORT))

# listen for incoming connections
server_socket.listen(5)

# list to store all connected clients
clients = []

def handle_client(client_socket, client_address):
    # add the client to the list of connected clients
    clients.append(client_socket)

    # send a welcome message to the client
    client_socket.send(b"Welcome to the chat room!\n")

    while True:
        # receive a message from the client
        message = client_socket.recv(1024).decode()

        if message == "list":
            # send a list of all connected clients to the client
            client_socket.send(b"Connected clients:\n")
            for client in clients:
                client_socket.send(f"{client.getpeername()[0]}:{client.getpeername()[1]}\n".encode())

        elif message == "exit":
            # remove the client from the list of connected clients and close the connection
            clients.remove(client_socket)
            client_socket.close()
            break

        else:
            # send the message to all connected clients (except the sender)
            for client in clients:
                if client != client_socket:
                    client.send(f"{client_address[0]}:{client_address[1]} says: {message}".encode())

while True:
    # accept an incoming connection
    client_socket, client_address = server_socket.accept()

    # create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
