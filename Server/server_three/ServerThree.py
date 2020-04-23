#
# Server Three
# Team: Server Python
# last-updated: 22/04/2020 by Team Server
#

# pip install psutil matplotlib pygame

import socket
import threading
import mylib as ml
from datetime import datetime
from tkinter import *
import os
import psutil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pygame

#
# Stampa su console della finestra tkinter pygame
#
def console_print(*text):
    console.config(state="normal")
    if len(text) > 0:
        out_str = str(text[0])
        text = text[1:]
        for t in text:
            out_str = out_str + " " + str(t)
        console.insert("end", out_str + "\n")
    else:
        console.insert("end", "\n")
    console.config(state="disabled")
    console.see("end")

#
# Stampa sulla lista utenti della finestra tkinter pygame
#
def userlist_print(*text):
    userList.config(state="normal")
    if len(text) > 0:
        out_str = str(text[0])
        text = text[1:]
        for t in text:
            out_str = out_str + " " + str(t)
        userList.insert("end", out_str + "\n")
    else:
        userList.insert("end", "\n")
    userList.config(state="disabled")
    userList.see("end")

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
    update_users()

#
# Aggiornamento lista utenti
#
def update_users():
    userList.config(state="normal")
    userList.delete('1.0', END)
    for i, th in enumerate(running_thread):
        userlist_print(th.username, "("+ str(i) +")")
        userlist_print(th.address)
        userlist_print()
    userList.config(state="disabled")

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
            print(self.username, "è crashato")
            console_print(self.username, "è crashato")

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
                # console_print("\nConnessione di", username, "con parametri", addr)

                # Creazione thread, avvio e ritorno ad ascoltare
                svc = UserHandler(clientSocket, addr, username)
                svc.start()
                running_thread.append(svc)

                update_users()

                # print("Thread inizializzato con successo")
                # console_print("Thread inizializzato con successo")
            except ConnectionResetError:
                print("Client chiuso forzatamente dall'utente")
                console_print("Client chiuso forzatamente dall'utente")
            except Exception as e:
                print("Arresto del server in corso")
                console_print("Arresto del server in corso")

    def stop(self):
        global running_thread
        threadLock.acquire()
        for i in running_thread:
            i.stop()
        running_thread = []
        threadLock.release()
        self.serverSocket.close()
        self.serverSocket = None
        self.running = False


# Vettore che memorizza tutti i thread in esecuzione
running_thread = []

# Definizione del lock
threadLock = threading.Lock()

# Inizializzazione parametri finestra
win = Tk()
win.geometry("1055x600")
win.title("Server Three")
win.resizable(width=False, height=False)
psutil_this = psutil.Process(os.getpid())
psutil_this.cpu_percent(interval=0)

server_running = False
th_server = None
pygame.init()

btnImg_on = PhotoImage(file="img/bottone_on.png")
btnImg_off = PhotoImage(file="img/bottone_off.png")

#
# Gestione avvio e spegnimento del server
#
def start_stop_server():
    global server_running
    global th_server
    global btnOnOff, btnImg_off, btnImg_on
    if server_running: # OFF
        pygame.mixer.music.load("sound/off.wav")
        pygame.mixer.music.play()
        btnOnOff = Button(win, image=btnImg_off, command=start_stop_server, bd="0").place(x=900, y=460)
        th_server.stop()
        th_server = None
        update_users()
    else: # ON
        pygame.mixer.music.load("sound/on.wav")
        pygame.mixer.music.play()
        btnOnOff = Button(win, image=btnImg_on, command=start_stop_server, bd="0").place(x=900, y=460)
        print("Avvio del server")
        console_print("Avvio del server")
        th_server = Server()
        th_server.start()
    server_running = not server_running

#
# Gestione comandi
#
def cmdHandler(event=None):
    global running_thread
    if server_running:
        cmd = cmdLine.get()
        if len(cmd) != 0:
            if cmd[0] == "/":
                cmd = cmd.lower().split(" ")
                if cmd[0] == "/kick":
                    if cmd[1] == "all":
                        threadLock.acquire()
                        for th in running_thread:
                            th.stop()
                        running_thread = []
                        threadLock.release()
                    else:
                        try:
                            th = running_thread[int(cmd[1])]
                            remove_connection(th.socket)
                        except Exception:
                            pass
            else:
                console_print(cmd)
                forward(None, "[SERVER]", cmd)
    else:
        console_print("Server spento!")
    cmdLine.delete("0", "end")

# Console principale
console = Text(win, width=100, height=23, borderwidth=2, relief="groove")
console.grid(column=0, row=0)
console.config(state="disabled")

# Linea per input messaggi e comandi
cmdLine = Entry(win, width=133, borderwidth=3, relief="groove")
cmdLine.bind('<Return>', cmdHandler)
cmdLine.grid(column=0, row=1)

# Bottone accensione e spegnimento server
btnOnOff = Button(win, image=btnImg_off, command=start_stop_server, bd="0").place(x=900, y=460)

# Lista utenti (finestra a dx)
userList = Text(win, width=30, height=23, borderwidth=2, relief="groove")
userList.grid(column=1, row=0)
userList.config(state="disabled")


# Grafici ----------------------------------------------------------------------------------
x = [i for i in range(0, 100)]
y_cpu = [0 for i in range(0, 100)]
y_ram = [0 for i in range(0, 100)]

def cpu_graph_anim(i):
    y_cpu.pop(0)
    y_cpu.append(psutil_this.cpu_percent() / psutil.cpu_count())
    line_cpu.set_ydata(y_cpu)  # Aggiorna grafico
    return line_cpu,

def ram_graph_anim(i):
    y_ram.pop(0)
    y_ram.append(psutil_this.memory_percent())
    line_ram.set_ydata(y_ram)  # Aggiorna grafico
    return line_ram,

fig = plt.Figure()
fig.set_size_inches(8.06, 2)

canvas = FigureCanvasTkAgg(fig, master=win)
canvas.get_tk_widget().grid(column=0,row=2)
ax = fig.add_subplot(111)
ax.axis(ymin=0.0, ymax=100.0, xmin=0.0, xmax=100.0)
ax.set_xticklabels([])
ax.set_ylabel('%', rotation=180)
line_cpu, = ax.plot(x, y_cpu, label="CPU")
line_ram, = ax.plot(x, y_ram, label="RAM")
ax.legend()
anim = animation.FuncAnimation(fig, cpu_graph_anim, None, interval=1000, blit=False, cache_frame_data=False)
anim2 = animation.FuncAnimation(fig, ram_graph_anim, None, interval=1000, blit=False, cache_frame_data=False)
# Fine grafici -----------------------------------------------------------------------------


# Visualizza
win.mainloop()
