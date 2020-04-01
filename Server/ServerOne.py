#
# Server One
# Team: Sandro Gallo
# last-updated: 26/03/2020 by Sandro
#

import socket
import mylib as ml

# Create a socket object (server)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# and Bind it to the addr:port
serverSocket.bind((ml.HOST, ml.PORT))
print("Server One started on", ml.HOST, ":", ml.PORT)

# Wait for client connection.
serverSocket.listen(5)
while True:
    # Wait for a connection request from any client
    print("\nwaiting a client connection ...")
    (clientSocket, addr) = serverSocket.accept()
    print('Got connection from', addr)
    # receiving a message from client
    msg = ml.strReceive(clientSocket)
    print("Received message: ", msg)
    # Close the connection
    clientSocket.close()
    if msg=='quit':
        break
print("Server terminated.")
