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
kicked_clients=[]

def on_new_client(clientsocket, addr):
    username = obten_nombre(clientsocket)
    send_log(f"{username} se ha conectado al chat.")  # Mensaje de registro
    while True:
        msg = get_msg(clientsocket)
        if msg.startswith("msg "):
            parts = msg.split(" ", 2)
            if len(parts) >= 3:
                recipient_name = parts[1]
                whisper_msg = parts[2]
                found_recipient = False
                for index, name in enumerate(names):
                    if name == recipient_name:
                        send_msg(f'(Susurro de {username}) : {whisper_msg}', clients[index])
                        found_recipient = True
                        break
                if not found_recipient:
                    send_msg(f'El destinatario "{recipient_name}" no está conectado o no existe.', clientsocket)
        elif msg.startswith("/KICK "):
            parts = msg.split(" ", 2)
            if len(parts)==3:
                kicker_name = names[clients.index(clientsocket)]
                target_name = parts[1]
                kick_user(kicker_name, target_name)        
        else:
            charla = username + ' : '+ msg
            send_log(charla)
            print(username, ' : ', msg)
    clientsocket.close()

def send_msg(msg, conna):
    conna.send(msg.encode())

def send_log(msg):
    for c in clients:
        if c not in kicked_clients:  # Exclude kicked clients from the log
            send_msg(msg, c)

def obten_nombre(conna):
    dataa = "Introduzca su nombre: "
    send_msg(dataa, conna)
    nombre = get_msg(conna)
    nombre = comp_nombre(nombre, conna)
    names.append(nombre)
    return nombre

def comp_nombre(nom, conna):
    for name in names:
        if nom == name:
            send_msg("Nombre ya seleccionado\n", conna)
            return obten_nombre(conna)
    return nom


def get_msg(conna):
    msg = conna.recv(20480).decode()
    return msg

def send_private_msg(sender, recipient, private_msg):
    found = False
    for conn, name in names.items():
        if name == recipient:
            send_msg(f'(Private) {sender} : {private_msg}', conn)
            found = True
            break
        if not found:
            send_msg(f'El destinatario "{recipient}" no está conectado o no existe.', names[sender])

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


server = "0.0.0.0"
port = 65433 
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
    
