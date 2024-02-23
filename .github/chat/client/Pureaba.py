import socket
import sys
import os

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

##server = input("Enter server IP: ")
##print(server)
##
##port = int(input("Enter port: "))
##print(port)

def send_msg(msg):
    sock.sendall(msg.encode())

def get_msg():
    msg = sock.recv(2048).decode()
    return msg

server = "10.10.10.230"
port = 60000

sock.connect((server, port))
print("Connecting to " + server + " on port " + str(port) + "\n")

while True:
    #Send data
    msg = input("Escribe: ")
    print("Sending '" + msg + "'")
    send_msg(msg)

    #Response
    #amnt_exp = len(msg)
    #data = sock.recv(2048)
    data = get_msg()

    if data == "exit":
        print("\nClosing connection")
        sock.close()
    else:
        print("Received: \n" + data)
