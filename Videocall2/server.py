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
clients_vc={}
clients_msg={}
broadcast_clients={}

def broadcast():
    while(True):
        mess="Enter the message which you want to broadcast"
        print(mess)
        ans=input()
        
            
            
        for client in broadcast_clients:
            broadcast_clients[client].send(ans.encode('utf-8'))

def first_func(sender_socket):
    username = sender_socket.recv(1024).decode('utf-8')
    matchmaking(sender_socket,username)
def matchmaking(sender_socket,username):   
    if username in clients_vc:
        reciever_socket=clients_vc[username]
        handle_client_vc(sender_socket,reciever_socket)
    else:
        time.sleep(1)
        matchmaking(sender_socket,username)

all_msg=[]
def handle_client_msg(client_socket):
    while True:
        try:
            # Receive data from the client
            print("I am here")
            data = client_socket.recv(1024).decode('utf-8')
            print(data)
            if not data:
                break

            # Split the message into recipient and message content
            recipient,message = data.split(":", 1)
            print("Message Recieved")

            # Find the recipient client socket and send the message
            if recipient=='all':
                for client in clients_msg:
                    if(client_socket==clients_msg[client]):
                        all_msg.append([[client],[message]])
                for client in clients_msg:
                    recipient_socket = clients_msg[client]
                    recipient_socket.send(message.encode('utf-8'))

            if recipient in clients_msg:
                recipient_socket = clients_msg[recipient]
                recipient_socket.send(message.encode('utf-8'))          
            else:
                client_socket.send(f"Recipient '{recipient}' not found.".encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
            break

    # Remove the disconnected client
    for username, socket in clients_msg.items():
        if socket == client_socket:
            del clients_msg[username]
            break

    client_socket.close()




def handle_client_vc(sender_socket,reciever_socket):
    

    while True:
        try:


            packet = sender_socket.recv(4096)
            reciever_socket.sendall(packet)
                    

        except:
            print("Error in recieving")
            break

        
                
              
    client_socket.close()
broadcast_thread_msg=threading.Thread(target=broadcast)
broadcast_thread_msg.start()
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    # Prompt the client for their username
    # client_socket.send("Enter your username: ".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8')
    if(username[0]=='b'):
        broadcast_clients[username[1:]]=client_socket
    if(username[0]=='v'):
        clients_vc[username[1:]] = client_socket
        client_thread_vc = threading.Thread(target=first_func, args=(client_socket,))
        client_thread_vc.start()
    if(username[0]=='m'):
        clients_msg[username[1:]] = client_socket
        client_thread_msg = threading.Thread(target=handle_client_msg, args=(client_socket,))
        client_thread_msg.start()


    # Create a thread to handle the client
    
    

    