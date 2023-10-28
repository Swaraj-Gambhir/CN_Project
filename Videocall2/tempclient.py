import socket
import threading
format='utf-8'
IP = socket.gethostbyname(socket.gethostname())
port=12345
SIZE=1024
address=(IP,port)




    # Creating a TCP socket
client_socket_ft = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket_ft.connect(address)
    # filename=input("Enter the name of the file")
    # client_socket.send(filename.encode(format))
def send_file():
    fname=input("Enter the name of the file")
    f=open(fname,'r')
    client_socket_ft.send(fname.encode(format))
        # client_socket.wait()
    while True:
            print("Reading File")
            line = f.readline()
            if not line:
                break
        
            client_socket_ft.send(line.encode(format))
        
    client_socket_ft.send('!END'.encode(format))
    print("Finish Sending")
    mess=client_socket_ft.recv(1024).decode(format)
    print(mess)
    f.close()
    client_socket_ft.close()
def recieve_file():
    try:
        fname=client_socket_ft.recv(10).decode(format)
        f=open(fname,'w+')
        DISCONNECT_MSG='!END'
        connected = True
        while connected:#loop will run until disconnect command from client
            msg = client_socket_ft.recv(1024).decode(format)#size=1024 utf-8 is format
            print("Message Recieved")
            if msg == DISCONNECT_MSG:
                print("Finishing")
                connected = False#stopping while loop
            else:
                f.write(msg)
                print("Message writing")
        mess="File Recieved"
        client_socket_ft.send(mess.encode(format))

        f.close()
        socket.close()
    except:
         print("Error")

message = "Enter your username"
print(message)
user=input()
recieve_file_thread=threading.Thread(target=recieve_file)
recieve_file_thread.start()
send_file_thread=threading.Thread(target=send_file)
send_file_thread.start()


    



