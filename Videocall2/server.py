import socket
import threading
import time


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP=socket.gethostbyname(socket.gethostname())
server_address = (IP, 12345)
server_socket.bind(server_address)
server_socket.listen(5)
print("Server is listening for incoming connections...")
clients={}

def handle_client(client_socket):
    while True:
        print(1)
        # recipient_socket = clients[usr]
        message='HI'
        client_socket.send(message.encode('utf-8'))
        time.sleep(1)
    client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    # Prompt the client for their username
    # client_socket.send("Enter your username: ".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8')
    clients[username] = client_socket

    # Create a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()