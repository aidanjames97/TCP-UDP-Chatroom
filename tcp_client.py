# Assignment: TCP Simple Chat Room - TCP Client Code Implementation
# **Libraries and Imports**: 
#    - Import the required libraries and modules. 
#    You may need sys, socket, argparse, select, threading (or _thread) libraries for the client implementation.
#    Feel free to use any libraries as well.
import threading
import socket
import argparse
import sys

# **Global Variables**:
#    - IF NEEDED, Define any global variables that will be used throughout the code.
allowed = True

# **Function Definitions**:
#    - In this section, you will implement the functions you will use in the client side.
#    - Feel free to add more other functions, and more variables.
#    - Make sure that names of functions and variables are meaningful.
#    - Take into consideration error handling, interrupts,and client shutdown.
def run(clientSocket, clientname):
    arr = f"{str(clientname)} + $CONECT$"
    clientSocket.send(arr.encode())

    receiveThread = threading.Thread(target=receiveMessages, args=(clientSocket,clientname))
    receiveThread.daemon = True
    receiveThread.start()

    # the main client function
    try:
        print(f"client '{clientname}' ready for conversation:")
        while True:
            message = input(f"{clientname}: ")
            if message == '':
                if allowed != False:
                    clientSocket.send((str(clientname) + " disconnected").encode())
                break
            if allowed == False:
                print("server quit, message unable to send, closing connection")
                break
            clientSocket.send((str(clientname) + ": " + message).encode())

    except Exception as e:
        print(f'{e}, caught, closing ...')

# function to handle reception of servers message and print
def receiveMessages(clientSocket, clientName):
    global allowed
    while True:
        try:
            message = clientSocket.recv(1024).decode()
            if not message:
                print("server closed the connection")
                allowed = False
                break
            sys.stdout.write(f"\r{message}\n{clientName}: ")
            sys.stdout.flush()
        except ConnectionResetError:
            print("connection to the server was closed")
            break

    # loop is over close, here because thread needs to close it in order to avoid error
    clientSocket.close()    

# **Main Code**:  
if __name__ == "__main__":
    print("\n ---> Main Function Started TCP Client <---")
    print("     - hit entre at any time to close the client\n")

    parser = argparse.ArgumentParser(description='Argument Parser')
    parser.add_argument('name')  # to use: python tcp_client.py username
    args = parser.parse_args()
    client_name = args.name
    server_addr = '127.0.0.1'
    server_port = 9301

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
    client_socket.connect((server_addr, server_port))

    run(client_socket, client_name)
    print('---> client socket closed <---\n')