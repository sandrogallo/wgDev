#
# Server One
# Team: Sandro Gallo
# last-updated: 26/03/2020 by Sandro
#

import socket
import threading
import mylib as ml
from datetime import datetime

class Service(threading.Thread):
    def __init__(self, s, a):               # s: clientSocket - a: address
       threading.Thread.__init__(self)
       self.s = s
       self.a = a

    def run(self):
        while True:
            # receiving a message from client
            msg = ml.strReceive(self.s).split("~")
            # msg[0] - Username
            # msg[1] - Contenuto massaggio

            now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            if msg[1] == 'quit':
                print("["+now+"]", msg[0], "ha abbandonato la chat")
                # Close the connection
                self.s.close()
                break;

            print("["+now+"]", msg[0] + ": " + msg[1])


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
    svc = Service(clientSocket,addr)
    svc.start()
print("Server terminated.")
