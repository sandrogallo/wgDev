#
# ClientTwo for Server Two
# Team: Server Python
# last-updated: 02/04/2020 by Team Server
#

import socket
import threading
import mylib as ml

#
# Thread per ascoltare i messaggi in entrata
#
class Listener(threading.Thread):
    def __init__(self, s): # s: clientSocket - a: address
       threading.Thread.__init__(self)
       self.s = s
       self.running = True;

    def run(self):
        while self.running:
            msg = ml.strReceive(self.s)
            print(msg)

    def stop(self):
        self.running = False


# Creazione socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Client connesso a", ml.HOST)

#
# Connessione a HOST e PORT
#
clientSocket.connect((ml.HOST, ml.PORT))
print("Connesso al server", ml.HOST, ":", ml.PORT)

#
# Inserimento username
#
username = input("Username: ")
ml.strSend(clientSocket, username) # Il primo messaggio che il server si aspetta è l'username

#
# Avvio thread che ascolta i messaggi in entrata
#
listener = Listener(clientSocket)
listener.start()

while True:
    # Input del messaggio dell'utente
    msg = input("")

    if(len(msg) != 0): # Verifica se il messaggio è vuoto
        # Invio del messaggio
        ml.strSend(clientSocket, msg)

        # Arresto del client
        if msg=="quit":
            listener.stop()
            listener.join()
            break

# Chiude il socket
clientSocket.close()
print("Connessione terminata.")
