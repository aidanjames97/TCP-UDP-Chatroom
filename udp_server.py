# Assignment: UDP Simple Chat Room - UDP Server Code Implementation

# **Libraries and Imports**: 
#    - Import the required libraries and modules. 
#    You may need socket, select, time libraries for the client.
#    Feel free to use any libraries as well.
import socket
import threading

# **Global Variables**:
#    - IF NEEDED, Define any global variables that will be used throughout the code.
RES_404 = "HTTP/1.1 404 Not Found\r\n\r\n"
RES_200 = "HTTP/1.1 200 OK\r\n\r\n"
clients = [] #list to add the connected client sockets

# **Function Definitions**:
#    - In this section, you will implement the functions you will use in the server side.
#    - Feel free to add more other functions, and more variables.
#    - Make sure that names of functions and variables are meaningful.
def run(serverSocket, serverPort):
    serverSocket.bind(('127.0.0.1', serverPort))

    thread = threading.Thread(target=handleClient)
    thread.daemon = True
    thread.start()

    while True:
        pass

# runs for each client
def handleClient():
    try:
        while True:
            message, clientAddress = serverSocket.recvfrom(1024)
            message = message.decode()
            if not message:
                break
                
            if ": disconnected." in message:
                clients.remove(clientAddress)
                print(message)  
            else:
                if clientAddress not in clients:
                    clients.append(clientAddress)
                    message = message.split()
                    print(f'User {message[0]} joined from address: {clientAddress}')

                if "$CONECT$" not in message:
                    print(f"Message received from {clientAddress}: {message}")

            # Broadcast the message to all connected clients
            if "$CONECT$" not in message:
                for client in clients:
                    if client != clientAddress:
                        serverSocket.sendto(message.encode(), client)
    except Exception as e:
        print(f"{e} caught, closing ...")

# **Main Code**:  
if __name__ == "__main__":
    print("\n ---> Chatroom <---\n")
    print("This is server side")
    
    try:
        serverPort = 9301  # Set the `serverPort` to the desired port number (e.g., 9301).
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Creating a UDP socket.
        print(f"I am ready to receive connections on port {serverPort}")
        run(serverSocket, serverPort)  # Calling the function to start the server.
    except KeyboardInterrupt:
        print(": Keyboard interrupt, shutting down ...")
    except Exception as e:
        print(f"{e} caught ...")
        

    print("---> Chatroom Closed <---\n")