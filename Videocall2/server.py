import socket
import threading
import time
import cv2,struct,pickle


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP=socket.gethostbyname(socket.gethostname())
server_address = (IP, 12345)
server_socket.bind(server_address)
server_socket.listen(5)
print("Server is listening for incoming connections...")
clients={}

def handle_client(client_socket):
    while True:
        
        if client_socket:
            cap = cv2.VideoCapture(cv2.CAP_DSHOW)
            while(cap.isOpened()):
                img,frame = cap.read()
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
                cv2.imshow('Video from Server',frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key ==ord('q'):
                    client_socket.close()
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