#
# Server Two
# Team: Server Python
# last-updated: 15/04/2020 by Team Server
#

import socket
import threading
import mylib as ml
from datetime import datetime

# Vettore che memorizza tutte le connessioni
connessioni = []

#
# Messaggio di chiusura forzata del client
#
def client_closed(my_socket, username):
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S") # Data corrente
    out = "["+now+"] " + username + " ha chiuso il client"
    print(out)
    send_to_all(my_socket, username, out)
    connessioni.remove(my_socket)

#
# Inoltra a tutti gli altri client il messaggio
#
def send_to_all(my_socket, username, msg):
    for socket in connessioni:
        try:
            if(socket != my_socket):
                ml.strSend(socket, username + "> " + msg)
        except:
            print(socket, "non ha ricevuto")

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
                    out = "["+now+"] " + self.username + " ha abbandonato la chat"
                    print(out)
                    ml.strSend(self.s, out) # Messaggio di termine
                    send_to_all(self.s, self.username, out)
                    self.s.close()
                    connessioni.remove(self.s)
                    break;

                print("["+now+"]", self.username + ": " + msg)
                send_to_all(self.s, self.username, msg)
        except ConnectionResetError: # Nel caso il client venga chiuso dalla X
            client_closed(self.s, self.username)
        except ValueError: # Nel caso il client venga chiuso dalla X
            client_closed(self.s, self.username)


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
    print("\nAttesa di una connessione...\n")
    (clientSocket, addr) = serverSocket.accept()

    username = ml.strReceive(clientSocket)
    # Connessione ricevuta, estrae l'username
    print("\nConnessione di", username, "con parametri", addr)
    connessioni.append(clientSocket)

    # Creazione thred, avvio e ritorno ad ascoltare
    svc = Service(clientSocket, addr, username)
    svc.start()
    print("Thread inizializzato con successo")

print("Server terminated.")
