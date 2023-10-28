import socket
import threading
IP = socket.gethostbyname(socket.gethostname())
format='utf-8'
port=12345
address=(IP,port)

def handle_client(socket,address):
    fname=socket.recv(10).decode(format)
    f=open(fname,'w+')
    DISCONNECT_MSG='!END'
    connected = True
    while connected:#loop will run until disconnect command from client
        msg = socket.recv(1024).decode(format)#size=1024 utf-8 is format
        print("Message Recieved")
        if msg == DISCONNECT_MSG:
            print("Finishing")
            connected = False#stopping while loop
        else:
            
            f.write(msg)
            print("Message writing")
    mess="File Recieved"
    socket.send(mess.encode(format))

    f.close()
    socket.close()

# Creating a TCP pocket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Binding of client
server.bind(address)
server.listen(5)
print("Server listening.......")

while True:
    client_socket, client_address = server.accept()
    

    print(f"connected from {client_address[0]}:{client_address[1]}")
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
