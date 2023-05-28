import socket
import threading
import time
import random
import os

HOST = ''
PORT = 1234

def send_data(client_socket):
    while True:
        # Delay for 5 seconds
        time.sleep(5)

        # Send data to the client
        pid = os.getpid()
        message = 'PID: ' + str(pid) + ' M: ' + str(random.randint(1, 100))
        client_socket.sendall(message.encode())

def receive_data(client_socket, client_address):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            # No data received, connection closed by client
            print("Connection closed by client:", client_address)
            break

        # Process the received data
        print("Received data:", data.decode())

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Server is listening on {}:{}".format(HOST, PORT))

while True:
    # Accept incoming connections
    client_socket, client_address = server_socket.accept()
    print("Received connection from:", client_address)

    # Start the send_data and receive_data threads
    send_thread = threading.Thread(target=send_data, args=(client_socket,))
    receive_thread = threading.Thread(target=receive_data, args=(client_socket, client_address))

    send_thread.start()
    receive_thread.start()
