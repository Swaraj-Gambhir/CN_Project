# import socket

# HOST = '127.0.0.1'
# PORT = 2341

# def receive_file(filename):
#     # Create a socket connection.
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind((HOST, PORT))
#     s.listen(1)
#     conn, addr = s.accept()
#     print('Connected by', addr)

#     with open(filename, 'wb') as file:
#         while True:
#             data = conn.recv(1024)  # Receive data in chunks (adjust chunk size as needed).
#             if not data:
#                 break
#             file.write(data)
    
#     conn.close()
#     print(f'{filename} received from client')

# # Specify the filenames you want to receive
# file_names = ['/home/shashank/Documents/LAB_PROJECT_CN/Shiv.mp4', '/home/shashank/Documents/LAB_PROJECT_CN/image.jpeg', '/home/shashank/Documents/LAB_PROJECT_CN/document.pdf']

# for file_name in file_names:
#     receive_file(file_name)
import socket

HOST = '127.0.0.1'
PORT = 4438

def receive_file(filename):
    # Create a socket connection.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)

    buffer = b''  # Initialize an empty binary buffer

    while True:
        data = conn.recv(1024)  # Receive data in chunks (adjust chunk size as needed).
        if not data:
            break
        buffer += data  # Accumulate the chunks in the buffer
    
    with open(filename, 'wb') as file:
        file.write(buffer)  # Write the entire buffer to the file

    conn.close()
    print(f'{filename} received from client')

# Specify the filenames you want to receive
#file_names = ['recv_vid.mp4', 'received_image.jpeg', 'received_document.pdf']
file_name= 'recv_vid.txt'
receive_file(file_name)
#for file_name in file_names:
#    receive_file(file_name)
