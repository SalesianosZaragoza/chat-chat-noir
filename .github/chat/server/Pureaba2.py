import socket
import sys
import os
import subprocess

#Create a TCP/IP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)




def send_msg(msg):
    conn.sendall(msg.encode())

def get_msg():
    msg = conn.recv(2048).decode()
    return msg

server = "10.10.14.230"
port = 60000

#Config
sock.bind((server, port))
print("Bound to " + server + " on port " + str(port) + "\n")

sock.listen(1)
while True:
    print('Waiting for a connection...') # inside the loop, not before it
    conn, caddr = sock.accept()
    print("Connected!\n")

    while True:
        print("Waiting for a command...")
        data = get_msg()
        if data == "hola":
            print("estas")


        #Exit
        if data == "exit":
            print("\nConnection closed")
            conn.close()
            break # go back to the outer accept loop to get the next connection

        print("Received '" + data + "'")
        # ... etc. ...
        print()