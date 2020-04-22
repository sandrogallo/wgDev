#
# Server Three
# Team: Server Python
# last-updated: 22/04/2020 by Team Server
#

import socket
import threading
import mylib as ml
from datetime import datetime
from tkinter import *

#
# Stampa su console della finestra tkinter
#
def console_print(*text):
    console.config(state="normal")
    out_str = ""
    for t in text:
        out_str = out_str + " " + str(t)
    console.insert("end", out_str + "\n")
    console.config(state="disabled")
    console.see("end")

#
# Messaggio di chiusura forzata del client
#
def client_closed(my_socket, username):
    out = "["+timespamp()+"] " + username + " ha chiuso il client"
    print(out)
    console_print(out)
    forward(my_socket, username, out)

#
# Messaggio di chiusura con comando quit
#
def client_quitted(my_socket, username):
    out = "["+timespamp()+"] " + username + " ha abbandonato la chat"
    print(out)
    console_print(out)
    ml.strSend(my_socket, out) # Messaggio di termine
    forward(my_socket, username, out)

#
# Restituisce stringa formattata con ora corrente
#
def timespamp():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S") # Data corrente

#
# Inoltra a tutti gli altri client il messaggio
#
def forward(my_socket, username, msg):
    for th in running_thread:
        try:
            if(th.socket != my_socket):
                ml.strSend(th.socket, username + "> " + msg)
        except:
            console_print(th.socket, "non ha ricevuto")

#
# Ferma e cancella il thread della connessione passata come parametro
#
def remove_connection(socket):
    threadLock.acquire() # Blocca l'accesso alle variabili per gli altri thread
    for i, th in enumerate(running_thread):
        if th.socket == socket:
            running_thread[i].stop()
            del running_thread[i]
            break
    threadLock.release() # Rilascia il blocco

#
# Gestisce la connessione di un utente
#
class UserHandler(threading.Thread):
    def __init__(self, s, a, username):
       threading.Thread.__init__(self)
       self.socket = s
       self.address = a
       self.username = username
       self.running = True

    def run(self):
        try:
            while self.running:
                msg = ml.strReceive(self.socket) # Ricezione messaggio

                # Comando di uscita, il thread viene terminato
                if msg == 'quit':
                    client_quitted(self.socket, self.username)
                    remove_connection(self.socket)
                    break;

                now = timespamp()
                print("["+now+"]", self.username + ": " + msg)
                console_print("["+now+"]", self.username+":" , msg)
                forward(self.socket, self.username, msg)
        except ConnectionResetError: # Nel caso il client venga chiuso dalla X
            client_closed(self.socket, self.username)
            remove_connection(self.socket)
        except ValueError: # Nel caso il client venga chiuso dalla X
            client_closed(self.socket, self.username)
            remove_connection(self.socket)
        except Exception as e:
            remove_connection(self.socket)
            print(self.username, "rip")
            console_print(str(self.username), "rip")

    def stop(self):
        self.socket.close()
        self.socket = None
        self.running = False

#
# Gestisce l'apertura di nuove connessioni
#
class Server(threading.Thread):
    def __init__(self):
       threading.Thread.__init__(self)
       self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.serverSocket.bind((ml.HOST, ml.PORT))
       print("Server Three avviato su", ml.HOST, ":", ml.PORT)
       console_print("Server Three avviato su", ml.HOST, ":", ml.PORT)
       self.serverSocket.listen(5)
       self.running = True

    def run(self):
        while self.running:
            try:
                # Attesa di una connessione
                # print("\nAttesa di una connessione...\n")
                (clientSocket, addr) = self.serverSocket.accept()

                # Connessione ricevuta, estrae l'username
                username = ml.strReceive(clientSocket)

                print("\nConnessione di", username, "con parametri", addr)
                console_print("\nConnessione di", username, "con parametri", addr)

                # Creazione thred, avvio e ritorno ad ascoltare
                svc = UserHandler(clientSocket, addr, username)
                svc.start()
                running_thread.append(svc)
                print("Thread inizializzato con successo")
                console_print("Thread inizializzato con successo")
            except ConnectionResetError:
                print("Client chiuso forzatamente dall'utente")
                console_print("Client chiuso forzatamente dall'utente")
            except Exception:
                print("Rip")
                console_print("Rip")

    def stop(self):
        global running_thread
        threadLock.acquire()
        for i in running_thread:
            i.stop()
        threadLock.release()
        self.serverSocket.close()
        self.serverSocket = None
        self.running = False


# Vettore che memorizza tutti i thread in esecuzione
running_thread = []

# Definizione del lock
threadLock = threading.Lock()

server_running = False
th_server = None

def start_stop_server():
    global server_running
    global th_server
    if server_running:
        th_server.stop()
        server_running = not server_running
        print("Server terminato")
        console_print("Server terminato")
    else:
        print("Avvio del server")
        console_print("Avvio del server")
        th_server = Server()
        th_server.start()
        server_running = not server_running

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
