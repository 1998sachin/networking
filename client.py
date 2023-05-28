import socket
import threading
import random
import time
HOST = '127.0.0.1'
PORT = 1234

def send_data(client_socket):
    while True:
        # Delay for 5 seconds
        time.sleep(5)

        # Send data to the server
        message = 'Client data: ' + str(random.randint(1, 100))
        client_socket.sendto(message.encode(), (HOST, PORT))

def receive_data(client_socket):
    while True:
        # Receive data from the server
        data, server_address = client_socket.recvfrom(1024)
        if not data:
            # No data received, connection closed by server
            print("Connection closed by server")
            break

        # Process the received data
        print("Received data:", data.decode())

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Start the send_data and receive_data threads
send_thread = threading.Thread(target=send_data, args=(client_socket,))
receive_thread = threading.Thread(target=receive_data, args=(client_socket,))

send_thread.start()
receive_thread.start()

# Join the threads to wait for their completion
send_thread.join()
receive_thread.join()
