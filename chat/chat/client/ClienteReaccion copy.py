import socket
import sys
import os
import time
import threading

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

##server = input("Enter server IP: ")
##print(server)
##
##port = int(input("Enter port: "))
##print(port)

def send_msg(msg):
    sock.send(msg.encode())

def get_msg():
    while True:
        msg = sock.recv(20480).decode()
        if msg == "exit":
            print("\nClosing connection")
            sock.close()
        else:
            print(msg)
        

server = "10.10.10.223"
port = 65433


sock.connect((server, port))
print("Connecting to " + server + " on port " + str(port) + "\n")
dataa = sock.recv(20480).decode()
msg = input(dataa)
send_msg(msg)
while True:
    #Send data
    t1 = threading.Thread(target=get_msg, args=())
    t1.start()
    msg = input()
    send_msg(msg)


    #Response
    #amnt_exp = len(msg)
    #data = sock.recv(2048)
   

    
