#
# Server Two
# Team: Server Python
# last-updated: 02/04/2020 by Team Server
#

import socket
import threading
import mylib as ml
from datetime import datetime

def client_closed(username):
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S") # Data corrente
    print("["+now+"]", username, "ha chiuso il client")

class Service(threading.Thread):
    def __init__(self, s, a, username): # s: clientSocket - a: address
       threading.Thread.__init__(self)
       self.s = s
       self.a = a
       self.username = username

    def run(self):
        try:
            while True:
                msg = ml.strReceive(self.s) # Ricezione messaggio

                now = datetime.now().strftime("%d-%m-%Y %H:%M:%S") # Data corrente

                # Comando di uscita, il thread viene terminato
                if msg == 'quit':
                    print("["+now+"]", self.username, "ha abbandonato la chat")
                    self.s.close()
                    break;

                print("["+now+"]", self.username + ": " + msg)
        except ConnectionResetError:
            client_closed(self.username)
        except ValueError:
            client_closed(self.username)


#
# Creazione socket e ascolto su HOST e PORT
#
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((ml.HOST, ml.PORT))
print("Server Two avviato su", ml.HOST, ":", ml.PORT)

# Il server ascolta
serverSocket.listen(5)
while True:
    # Attesa di una connessione
    print("\nwaiting a client connection ...")
    (clientSocket, addr) = serverSocket.accept()

    # Connessione ricevuta, estrae l'username
    print('Got connection from', addr)
    username = ml.strReceive(clientSocket)

    # Creazione thred, avvio e ritorno ad ascoltare
    svc = Service(clientSocket, addr, username)
    svc.start()

print("Server terminated.")
