import socket
import threading,time,os
IP = socket.gethostbyname(socket.gethostname())
format='utf-8'
port=12345
address=(IP,port)
clients_ft={}
clients_ft_rcv={}
def second_func(sender_socket):
    username1 = sender_socket.recv(1024).decode('utf-8')
    matchmaking1(sender_socket,username1)
reciever_socket_list=[]
def matchmaking1(sender_socket,username1): 
    if username1=='all':
        for i in clients_ft_rcv:
            reciever_socket_list.append(clients_ft_rcv[i])
            print("matchmaking done")
            
        fname = sender_socket.recv(1024).decode('utf-8')
        print(fname)
        handle_client_ft(sender_socket,reciever_socket_list,fname)
    elif username1 in clients_ft:
        reciever_socket=clients_ft[username1]
        print("matchmaking done")
        
        fname = sender_socket.recv(1024).decode('utf-8')
        print(fname)
        handle_client_ft(sender_socket,reciever_socket,fname)
        
            
    else:
        time.sleep(1)
        matchmaking1(sender_socket,username1)

    
def handle_client_ft(sender_socket,reciever_socket,fname):
    print("Handling CLient Now")
    
    buffer = b''  # Initialize an empty binary buffer

    while True:
        data = sender_socket.recv(1024)  # Receive data in chunks (adjust chunk size as needed).
        if not data:
            break
        buffer += data  # Accumulate the chunks in the buffer
    
    with open(fname, 'wb') as file:
        file.write(buffer)  # Write the entire buffer to the file

    sender_socket.close()
    print(f'{fname} received from client')
    file.close()
    
    
    if (type(reciever_socket)==list):
        for reciever_socke in reciever_socket:
            reciever_socke.send(fname.encode('utf-8'))
            file_size = os.path.getsize(fname)
            reciever_socke.send(str(file_size).encode('utf-8'))
            try:
                with open(fname, 'rb') as file:
                    while True:
                        data = file.read(1024)  # Read data in chunks (adjust chunk size as needed).
                        if not data:
                            break  # End of file
                        reciever_socke.send(data)
            
            except Exception as e:
                print(f"Error while sending {fname}: {str(e)}")
            
            
            print(f'{fname} Sent to Client')
    else:
        reciever_socket.send(fname.encode('utf-8'))
        file_size = os.path.getsize(fname)
        reciever_socket.send(str(file_size).encode('utf-8'))
        try:
            with open(fname, 'rb') as file:
                while True:
                    data = file.read(1024)  # Read data in chunks (adjust chunk size as needed).
                    if not data:
                        break  # End of file
                    reciever_socket.send(data)
        
        except Exception as e:
            print(f"Error while sending {fname}: {str(e)}")
        
        
        print(f'{fname} Sent to Client')


        


# Creating a TCP pocket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Binding of client
server.bind(address)
server.listen(5)
print("Server listening.......")

while True:
    client_socket, client_address = server.accept()
    username = client_socket.recv(1024).decode('utf-8')
    if(username[0]=='0'):
        clients_ft_rcv[username[1:]]=client_socket
    clients_ft[username[1:]]=client_socket

    print(f"connected from {client_address[0]}:{client_address[1]}")

    client_thread = threading.Thread(target=second_func, args=(client_socket,))
    client_thread.start()
