import socket
import threading
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = socket.gethostbyname(socket.gethostname())
server_address = (IP, 12345)
client_socket.connect(server_address)
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')     
            print(message)
        except Exception as e:
            print(f"Error: {e}")
            break

message = "Enter your username"
print(message)
user=input()

client_socket.send(user.encode('utf-8'))
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()



# cd Documents/Project/Videocall2