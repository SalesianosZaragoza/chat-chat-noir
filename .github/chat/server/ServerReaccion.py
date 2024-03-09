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

def on_new_client(clientsocket,addr):
    username = obten_nombre(clientsocket)
    send_log(f"{username} se ha conectado al chat.")  # Mensaje de registro
    while True:
        msg = get_msg(clientsocket)
        charla = username + ' : '+ msg
        send_log(charla)
        #do some checks and if msg == someWeirdSignal: break:
        print(username, ' : ', msg)
        #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
    clientsocket.close()

##server = input("Enter server IP: ")
##print(server)
##
##port = int(input("Enter port: "))
##print(port)

def send_msg(msg, conna):
    conna.send(msg.encode())

def send_log(msg):
    for c in clients:
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

#def send_private_msg(sender, recipient, private_msg):
 #   found = False
  #  for conn, name in names.items():
   #     if name == recipient:
    #       send_msg(f'(Private) {sender} : {private_msg}', conn)
    #       found = True
    #       break
    #   if not found:
#         send_msg(f'El destinatario "{recipient}" no está conectado o no existe.', names[sender])



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