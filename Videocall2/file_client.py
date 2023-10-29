import socket
import os

HOST = '127.0.0.1'
PORT = 4438

def send_file(filename):
    if not os.path.isfile(filename):
        print(f"File {filename} not found.")
        return

    # Create a socket connection.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    try:
        with open(filename, 'rb') as file:
            while True:
                data = file.read(1024)  # Read data in chunks (adjust chunk size as needed).
                if not data:
                    break  # End of file
                s.send(data)
    
    except Exception as e:
        print(f"Error while sending {filename}: {str(e)}")
    
    s.close
    print(f'{filename} Sent to Server')

# Specify the file paths you want to send
#file_paths = ['p.mp4', 'image.jpeg', 'document.pdf']
file_name = input("Enter the name of the file (eg. format-filename.mp4)\n")
send_file(file_name)
#for file_path in file_paths:
#    send_file(file_path)
