import socket
import sys
import os
import subprocess
import time
import threading


#Create a TCP/IP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clients = []
names = []
rooms = ["Sala 1"]
Chats = [[]]

def on_new_client(clientsocket,addr):
        username = obten_nombre(clientsocket)
        while True:
            msg, mostrar = get_msg(clientsocket, username)
            if not msg:
                break
            charla = username + ' : '+ msg
            if(mostrar):
                send_log(charla,clientsocket)
            #do some checks and if msg == someWeirdSignal: break:
            print(username, ' : ', msg)
        #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
        clientsocket.close()

def send_msg(msg, conna):
    conna.send(msg.encode())
def send_log(msg, conn):
    for c in clients:
        send_msg(msg, c)
def obten_nombre(conna):
    dataa = "Introduzca su nombre: "
    send_msg(dataa, conna)
    nombre, most = get_msg(conna, "a")
    nombre = comp_nombre(nombre, conna)
    names.append(nombre)
    return nombre
def comp_nombre(nom, conna):
    for name in names:
        if nom == name:
            send_msg("Nombre ya seleccionado\n", conna)
            return obten_nombre(conna)
    return nom

def ListChats(conna):
    data = ""
    for rom in rooms:
        data = data + rom + "\n"
    send_msg(data, conna)

def AddChat(b, conn):
    if b in rooms:
        send_msg("Ya existe " + b, conn)
    else:
        rooms.append(b)
        Chats.append([])

def JoinChannel(name, conn):
    if name in rooms:
        Chats[rooms.index(name)].append(conn)
        send_msg("Conectado a sala " + name, conn)

def get_msg(conna, name):
    mostrar = True
    msg = conna.recv(20480).decode()
    if msg == "/LIST":
        mostrar = False
        ListChats(conna)
    elif msg.find("/NEW") != -1:
        mostrar = False
        AddChat(msg[msg.find("/NEW") + 5:], conna)
    elif msg == "/EXIT":
        mostrar = False
        clients.remove(conna)
        names.remove(name)
        conna.close()
        sys.exit()
    elif msg.find("/JOIN") != -1:
        mostrar = False
        channel_name = msg[msg.find("/JOIN") + 6:]
        JoinChannel(channel_name, conna)
    return msg, mostrar

server = "0.0.0.0"
port = 65433 
##server = input("Enter server IP: ")
##print(server)
##
##port = int(input("Enter port: "))
##print(port)
all_threads = []
#Config
sock.bind((server, port))
print("Bound to " + server + " on port " + str(port) + "\n")

sock.listen(5)
while True:
    print('Waiting for a connection...') # inside the loop, not before it
    conn, caddr = sock.accept()
    print(f"Connected to!\n {caddr}")
    clients.append(conn)

    t1 = threading.Thread(target=on_new_client, args=(conn,caddr))
    t1.start()
    t1.join()

    all_threads.append(t1)
    #while True:
#        print("Waiting for a command...")
#        data = get_msg()
#        if data == "hola":
#            print("Me ha dicho hola")
#            send_msg("Gracias por saludar " + username)
#        else:
#            send_msg(" ")


        #Exit
#        if data == "exit":
#            print("\nConnection closed")
#            conn.close()
#            break # go back to the outer accept loop to get the next connection

 #       print("Received '" + data + "'")
  #      # ... etc. ...
   #     print()