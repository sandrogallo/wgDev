#
# testClient for Server One
# Team: Sandro Gallo
# last-updated: 26/03/2020 by Sandro
#

import socket
import mylib as ml

# Create a socket object (client)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Client started on", ml.HOST)

# Try to connect to the server
clientSocket.connect((ml.HOST, ml.PORT))
print("Connected to server", ml.HOST, ":", ml.PORT)

username = input("Username: ")

while True:
    # Request a message to user
    msg = input("Enter a message to send to the server: ")
    # Send a message to the server
    ml.strSend(clientSocket, username + "~" + msg)

    if msg=="quit":
        break

# Close the socket when done
clientSocket.close()
print("Connection closed.")
# input("press RETURN to terminate")
