#
# mylib
# define functions to proper send and receive strings on a socket
# Team: Sandro Gallo
# last-updated: 26/03/2020 by Sandro
#

import socket

# Set server addr:port
HOST = socket.gethostname()
PORT = 10101

def strSend(sock, str):
    strlen = '{:08d}'.format(len(str))
    sock.sendall(strlen.encode('utf-8'))
    sock.sendall(str.encode('utf-8'))

def strReceive(sock):
    data = ''
    l = int(sock.recv(8))
    while l > len(data):
        part = sock.recv(1024)
        if not part: break
        data += part.decode('utf-8')
    return str(data)
