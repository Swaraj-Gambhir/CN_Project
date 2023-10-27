import socket
import threading
import struct 
import cv2
import pickle,time
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = socket.gethostbyname(socket.gethostname())
server_address = (IP, 12345)
client_socket.connect(server_address)
def receive_frames():
    data = b""
    payload_size = struct.calcsize("Q")

    # sending our photo in a loop to the server
    try:
        while True:
            while len(data) < payload_size:
                packet = client_socket.recv(4096)
                
                if not packet: 
                    break
                data+=packet
            packed_msg = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q",packed_msg)[0]
            
            while len(data) < msg_size:
                data += client_socket.recv(4096)
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
    client_socket.send(rec.encode('utf-8'))
    time.sleep(5)
    while True: 
        if client_socket:
            cap = cv2.VideoCapture(cv2.CAP_DSHOW)
            while(cap.isOpened()):
                img,frame = cap.read()
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a))+a
                client_socket.send(message)
                cv2.imshow(f'Video from Server {user}',frame)
 
                key = cv2.waitKey(1) & 0xFF
                if key ==ord('q'):
                    client_socket.close()
message = "Enter your username"
print(message)
user=input()
# print("Enter the name of the reciever")
# rec=input()
# client_socket.send(rec.encode('utf-8'))

client_socket.send(user.encode('utf-8'))
receive_thread = threading.Thread(target=receive_frames)
send_thread= threading.Thread(target=send_frames)
receive_thread.start()
send_thread.start()



# cd Documents/Project/Videocall2