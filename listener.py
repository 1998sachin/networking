import socket
import threading
import time
import random
import os

HOST = ''
PORT = 1234

def send_data(client_address, server_socket):
    while True:
        # Delay for 5 seconds
        time.sleep(5)

        # Send data to the client
        pid = os.getpid()
        message = 'PID: ' + str(pid) + ' M: ' + str(random.randint(1, 100))
        server_socket.sendto(message.encode(), client_address)

def receive_data(server_socket):
    while True:
        # Receive data from the client
        data, client_address = server_socket.recvfrom(1024)
        if not data:
            # No data received, connection closed by client
            print("Connection closed by client")
            break

        # Process the received data
        print("Received data:", data.decode())

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server_socket.bind((HOST, PORT))
print("Server is listening on {}:{}".format(HOST, PORT))

while True:
    # Receive incoming datagrams
    data, client_address = server_socket.recvfrom(1024)
    print("Received connection from:", client_address)

    # Start the send_data and receive_data threads
    send_thread = threading.Thread(target=send_data, args=(client_address, server_socket,))
    receive_thread = threading.Thread(target=receive_data, args=(server_socket,))

    send_thread.start()
    receive_thread.start()
