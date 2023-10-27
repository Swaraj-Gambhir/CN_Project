import socket
import threading
import time
import cv2,struct,pickle


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP=socket.gethostbyname(socket.gethostname())
server_address = ('', 12345)
server_socket.bind(server_address)
server_socket.listen(5)
print("Server is listening for incoming connections...")
clients={}
def first_func(sender_socket):
    username = sender_socket.recv(1024).decode('utf-8')
    matchmaking(sender_socket,username)
def matchmaking(sender_socket,username):
    
    if username in clients:

        reciever_socket=clients[username]
        handle_client(sender_socket,reciever_socket)
    else:
        time.sleep(1)
        matchmaking(sender_socket,username)




def handle_client(sender_socket,reciever_socket):
    

    while True:
        try:


            packet = sender_socket.recv(4096)
            reciever_socket.sendall(packet)
                    

        except:
            print("Error in recieving")
            break

        
                
              
    client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    # Prompt the client for their username
    # client_socket.send("Enter your username: ".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8')
    clients[username] = client_socket

    # Create a thread to handle the client
    client_thread = threading.Thread(target=first_func, args=(client_socket,))
    client_thread.start()