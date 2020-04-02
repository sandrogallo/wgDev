#
# testClient for Server One
# Team: Sandro Gallo
# last-updated: 26/03/2020 by Sandro
#

import socket
import mylib as ml

# Create a socket object (client)
while True:
    username = input("Inserisci username: ")
    if(username == "quit"):
        break

    print("\nClient started on", ml.HOST)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try to connect to the server
    print("\nSearching for servers...")
    clientSocket.connect((ml.HOST, ml.PORT))
    print("Connected to server", ml.HOST, ":", ml.PORT, "\n")

    ml.strSend(clientSocket, username + "~" + "initjoined")

    while True:
        # Request a message to user
        msg = input("Enter a message to send to the server: ")
        # Send a message to the server
        ml.strSend(clientSocket, username + "~" + msg)

        if msg == "quit":
            print("\nDisconnessione dalla chat...")
            break

    # Close the socket when done
    clientSocket.close()
    print("Connection closed.\n")
    # input("press RETURN to terminate")

print("Program is closing.")
