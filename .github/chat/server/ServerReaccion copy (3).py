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
        send_log(f"{username} se ha conectado al chat.", conn)  # Mensaje de registro
        while True:
            msg, mostrar = get_msg(clientsocket, username)
            if not msg:
                break
            charla = username + ' : '+ msg
            if msg.startswith("/RENAME"):
                mostrar = False
                new_name = msg[len("/RENAME "):]
                if new_name:
                    if new_name not in names:
                        names[names.index(username)] = new_name
                        username = new_name
                        send_msg(f"Tu nombre ha sido cambiado a: {new_name}\n", clientsocket)
                    else:
                        send_msg("Este nombre ya está en uso. Por favor, elige otro.\n", clientsocket)
                else:
                    send_msg("El nombre no puede estar vacío.Por favor, ingresa un nombre válido.\n", clientsocket)
            if(mostrar):
                send_log(charla,clientsocket)
            #do some checks and if msg == someWeirdSignal: break:
            print(username, ' : ', msg)
        #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
        clientsocket.close()

def send_msg(msg, conna):
    conna.send(msg.encode())

def send_log(msg, conn):
    lista = 0
    for chat in Chats:
        if conn in chat:
            lista = Chats.index(chat)
    for c in Chats[lista]:
        send_msg(msg, c)

def obten_nombre(conna):
    dataa = "Introduzca su nombre: "
    send_msg(dataa, conna)
    nombre, most = get_msg(conna, "a")
    nombre = comp_nombre(nombre, conna)
    names.append(nombre)
    clients.append(conna)
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
    for chat in Chats:
        if conn in chat:
            chat.remove(conn)
    if name in rooms:
        Chats[rooms.index(name)].append(conn)
        send_msg("Conectado a sala " + name, conn)

def kick_user(target_name):
    con = clients[names.index(target_name)]
    for chat in Chats:
        if con in chat:
            chat.remove(con)
            send_msg("Has sido pateado de la sala", con)

def send_private_msg(sender, recipient, private_msg):
    if recipient in names:    
        con = names.index(recipient)
        send_msg(sender + " whispers" + private_msg, clients[con])
    else:
        con = names.index(sender)
        send_msg("No existe el usuario " + recipient, clients[con])
    

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
    elif msg.find("/KICK") != -1:
        mostrar = False
        target_name = msg[msg.find("/KICK") + 6:]
        kick_user(target_name)
    elif msg.find("/MSG") != -1:
        mostrar = False
        target_name = msg[msg.find("/MSG") + 5:msg.find(" ", msg.find("/MSG") + 5)]
        private_msg = msg[msg.find(" ", msg.find("/MSG") + 5):]
        send_private_msg(name, target_name, private_msg)
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
    

    t1 = threading.Thread(target=on_new_client, args=(conn,caddr))
    t1.start()

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