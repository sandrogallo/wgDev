#
# Server Three
# Team: Server Python
# last-updated: 21/04/2020 by Team Server
#

import socket
import threading
import mylib as ml
from datetime import datetime
from tkinter import *

# Vettore che memorizza tutte le connessioni
connessioni = []
running_thread = []
# Definizione del lock
threadLock = threading.Lock()


def insert_into_console(text):
    console.config(state="normal")
    console.insert("end", text + "\n")
    console.config(state="disabled")
    console.see("end")

#
# Messaggio di chiusura forzata del client
#
def client_closed(my_socket, username):
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S") # Data corrente
    out = "["+now+"] " + username + " ha chiuso il client"
    print(out)
    insert_into_console(out)
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
       self.running = True

    def run(self):
        try:
            while self.running:
                msg = ml.strReceive(self.s) # Ricezione messaggio

                now = datetime.now().strftime("%d-%m-%Y %H:%M:%S") # Data corrente

                # Comando di uscita, il thread viene terminato
                if msg == 'quit':
                    out = "["+now+"] " + self.username + " ha abbandonato la chat"
                    print(out)
                    insert_into_console(out)
                    ml.strSend(self.s, out) # Messaggio di termine
                    send_to_all(self.s, self.username, out)
                    self.s.close()
                    threadLock.acquire() # Blocca l'accesso alle variabili per gli altri thread
                    connessioni.remove(self.s)
                    threadLock.release() # Rilascia il blocco
                    break;

                print("["+now+"]", self.username + ": " + msg)
                insert_into_console("["+now+"]" + str(self.username) + ": " + str(msg))
                send_to_all(self.s, self.username, msg)
        except ConnectionResetError: # Nel caso il client venga chiuso dalla X
            client_closed(self.s, self.username)
        except ValueError: # Nel caso il client venga chiuso dalla X
            client_closed(self.s, self.username)
        except Exception:
            print(self.username, "rip")
            insert_into_console(str(self.username) + "rip")

    def stop(self):
        self.s = None
        self.running = False


#
# Creazione socket e ascolto su HOST e PORT
#


class Server(threading.Thread):
    def __init__(self):
       threading.Thread.__init__(self)
       self.running = False
       self.serverSocket = None

    def run(self):
        while True:
            while self.running:
                try:
                    # Attesa di una connessione
                    # print("\nAttesa di una connessione...\n")
                    (clientSocket, addr) = self.serverSocket.accept()

                    if self.running:
                        username = ml.strReceive(clientSocket)
                        # Connessione ricevuta, estrae l'username
                        print("\nConnessione di", username, "con parametri", addr)
                        insert_into_console("\nConnessione di " + str(username) + " con parametri " + str(addr))
                        connessioni.append(clientSocket)

                        # Creazione thred, avvio e ritorno ad ascoltare
                        svc = Service(clientSocket, addr, username)
                        svc.start()
                        running_thread.append(svc)
                        print("Thread inizializzato con successo")
                        insert_into_console("Thread inizializzato con successo")

                except ConnectionResetError:
                    print("Client chiuso forzatamente dall'utente")
                    insert_into_console("Client chiuso forzatamente dall'utente")
                except Exception:
                    print("Rip")
                    insert_into_console("Rip")

    def avvia(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((ml.HOST, ml.PORT))
        print("Server Three avviato su", ml.HOST, ":", ml.PORT)
        insert_into_console("Server Three avviato su" + str(ml.HOST) + ":" + str(ml.PORT))
        self.serverSocket.listen(5)
        self.running = True

    def stop(self):
        global connessioni
        global running_thread
        threadLock.acquire()
        connessioni = []
        for i in running_thread:
            i.stop()
        threadLock.release()
        self.serverSocket.close()
        self.serverSocket = None
        self.running = False

posso = False
th_server = Server()
th_server.start()

def start_stop_server():
    global posso
    if posso:
        th_server.stop()
        posso = not posso
        print("Server terminato")
        insert_into_console("Server terminato")
    else:
        print("Avvio del server")
        insert_into_console("Avvio del server")
        th_server.avvia()
        posso = not posso

# Inizializzazione parametri finestra
win = Tk()
win.geometry("1000x600")
win.title("Server Three")

console = Text(win, width=100, height=25, borderwidth=2, relief="groove")
console.grid(column=0, row=0)
console.config(state="disabled")

btnimg=PhotoImage(file="img/bottone.png")
btnOnOff = Button(win, image=btnimg, command=start_stop_server, bd="0").place(x=900, y=500)


# Visualizza
win.mainloop()
