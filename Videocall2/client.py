import socket
import threading
import struct 
import cv2
import pickle,time


# client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = socket.gethostbyname(socket.gethostname())
server_address = (IP, 12345)
client_socket_vc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket_msg=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP = socket.gethostbyname(socket.gethostname())
# server_address = (IP, 12345)
def switch(a):
    if(a==0):
        client_socket_vc.connect(server_address)
        user2='v'+user
        client_socket_vc.send(user2.encode('utf-8'))
        receive_vc_thread.start()
        send_vc_thread.start() 
    if(a==1):
        client_socket_msg.connect(server_address)
        user3='v'+user
        client_socket_msg.send(user3.encode('utf-8'))
        send_msg_thread.start()
        receive_msg_thread.start()
    

def call_func():
    a=int(input("Enter your choice"))
    switch(a)
    
def recieve_broadcastmessages():
    broadcast_socket.connect(server_address)
    user1='b'+user
    broadcast_socket.send(user1.encode('utf-8'))
    call_func()
    while True:
        try:
            packet= broadcast_socket.recv(1024).decode('utf-8')
            print("Message from server-->",packet)
        except:
            print("some error")
def receive_frames():
    data = b""
    payload_size = struct.calcsize("Q")

    # sending our photo in a loop to the server
    try:
        while True:
            while len(data) < payload_size:
                packet = client_socket_vc.recv(4096)
                
                if not packet: 
                    break
                data+=packet
            packed_msg = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q",packed_msg)[0]
            
            while len(data) < msg_size:
                data += client_socket_vc.recv(4096)
            frame = data[:msg_size]
            data  = data[msg_size:]
            vid = pickle.loads(frame)
            cv2.imshow(f"Video from Client {user}",vid)
            key = cv2.waitKey(1) & 0xFF
            if key  == ord('q'):
                break
    except:
        print("Video ended")
def send_frames():
    print("Enter the name of the reciever")
    rec=input()
    client_socket_vc.send(rec.encode('utf-8'))
    time.sleep(5)
    while True: 
        if client_socket_vc:
            cap = cv2.VideoCapture(cv2.CAP_DSHOW)
            while(cap.isOpened()):
                img,frame = cap.read()
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a))+a
                client_socket_vc.send(message)
                cv2.imshow(f'Video from Server {user}',frame)
 
                key = cv2.waitKey(1) & 0xFF
                if key ==ord('q'):
                    client_socket_vc.close()
def receive_messages():
    print("I am in Thread")
    while True:
        try:
            # Receive and print messages from the server
            message = client_socket_msg.recv(1024).decode('utf-8')
            print("You got a message")
            print("Message is",message)
            
            print("Enter the recipient's username (or 'all' for broadcast): ")
        except Exception as e:
            print(f"Error: {e}")
            break
def send_messages():
    while True:
        print("Enter the recipient's username (or 'all' for broadcast): ")
        recipient = input()
        print("Enter the message")
        messag=input()
        formatted_message=f"{recipient}:{messag}"
        client_socket_msg.send(formatted_message.encode('utf-8'))
message = "Enter your username"
print(message)
user=input()
# print("Enter the name of the reciever")
# rec=input()
# client_socket_vc.send(rec.encode('utf-8'))


recieve_broadcastmessages_thread=threading.Thread(target=recieve_broadcastmessages)
recieve_broadcastmessages_thread.start()
receive_vc_thread = threading.Thread(target=receive_frames)
send_vc_thread= threading.Thread(target=send_frames)
receive_msg_thread = threading.Thread(target=receive_messages)
send_msg_thread=threading.Thread(target=send_messages)



# cd Documents/Project/Videocall2
 