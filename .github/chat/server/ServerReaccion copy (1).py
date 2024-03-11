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
        send_log(f"{username} se ha conectado al chat.", conn) # Mensaje de registro
        while True:
            msg, mostrar = get_msg(clientsocket, username)
            if not msg:
                break
            charla = username + ' : '+ msg
            if(mostrar):
                send_log(charla,clientsocket)
            print(username, ' : ', msg)
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

def kick_user(kicker_name, target_name):
    global clients, names, kicked_clients
    if target_name in names:
        index = names.index(target_name)
        kicked_conn = clients[index]
        kicked_name = names.pop(index)
        clients.pop(index)
        kicked_clients.append(kicked_conn)
        send_log(f"{kicker_name} ha expulsado a {kicked_name} del chat.")
        send_msg("¡Has sido expulsado del chat!", kicked_conn)
        send_log(f"{kicked_name} ha sido expulsado del chat por {kicker_name}.")
        kicked_conn.close()
    else:
        send_msg(f'No se pudo encontrar al usuario "{target_name}" en la sala.', clients[names.index(kicker_name)])

def send_private_msg(sender, recipient, private_msg):
    found = False
    for conn, name in names.items():
        if name == recipient:
            send_msg(f'(Private) {sender} : {private_msg}', conn)
            found = True
            break
        if not found:
            send_msg(f'El destinatario "{recipient}" no está conectado o no existe.', names[sender])

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
        kick_user(name, target_name)
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
    clients.append(conn)

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