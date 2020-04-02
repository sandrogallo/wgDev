#
# ClientTwo for Server Two
# Team: Server Python
# last-updated: 02/04/2020 by Team Server
#

import socket
import mylib as ml

HOST = "pinco1710.ddns.net"

# Creazione socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Client connesso a", HOST)

#
# Connessione a HOST e PORT
#
clientSocket.connect((HOST, ml.PORT))
print("Connesso al server", HOST, ":", ml.PORT)

#
# Inserimento username
#
username = input("Username: ")
ml.strSend(clientSocket, username) # Il primo messaggio che il server si aspetta è l'username

while True:
    # Input del messaggio dell'utente
    msg = input("Inserisci messaggio> ")

    if(len(msg) != 0): # Verifica se il messaggio è vuoto
        # Invio del messaggio
        ml.strSend(clientSocket, msg)

        # Arresto del client
        if msg=="quit":
            break

# Chiude il socket
clientSocket.close()
print("Connessione terminata.")
