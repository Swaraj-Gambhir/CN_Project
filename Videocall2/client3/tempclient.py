import socket
import threading,os
format='utf-8'
IP = socket.gethostbyname(socket.gethostname())
port=12345
SIZE=1024
address=(IP,port)




    # Creating a TCP socket
client_socket_ft = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket_ft.connect(address)
def switch(a):
    if(a==0):
        recieve_file_thread.start()
    else:
        send_file_thread.start()
    # filename=input("Enter the name of the file")
    # client_socket.send(filename.encode(format))
def send_file():
    print("Enter the name of the reciever")
    rec=input()

    print("Enter filename")
    fname=input()
    
    client_socket_ft.send(rec.encode('utf-8'))
    client_socket_ft.send(fname.encode('utf-8'))

    try:
        with open(fname, 'rb') as file:
            while True:
                data = file.read(1024)  # Read data in chunks (adjust chunk size as needed).
                if not data:
                    break  # End of file
                client_socket_ft.send(data)
    
    except Exception as e:
        print(f"Error while sending {fname}: {str(e)}")
    
    client_socket_ft.close()
    print(f'{fname} Sent to Server')
    
    

    

        
def recieve_file():
    fname=client_socket_ft.recv(1024).decode(format)
    fsize=client_socket_ft.recv(1024).decode(format)
    fsize=int(fsize)
    count=(fsize//1024) +1
    print("File name",fname)
    buffer = b''  # Initialize an empty binary buffer

    while (count>0):
        data = client_socket_ft.recv(1024) 
        print("Hii") # Receive data in chunks (adjust chunk size as needed).
        count-=1
        buffer += data  # Accumulate the chunks in the buffer
    print("file recv")
    with open(fname, 'wb') as file:
        file.write(buffer)  # Write the entire buffer to the file
    print(f'{fname} received from client')
    client_socket_ft.close()
    
message = "Enter your username"
print(message)
user=input()
# client_socket_ft.send(user.encode('utf-8'))
recieve_file_thread=threading.Thread(target=recieve_file)

send_file_thread=threading.Thread(target=send_file)
a=int(input("1 to send 0 to recv"))
user=str(a)+user
client_socket_ft.send(user.encode('utf-8'))

switch(a)


    



