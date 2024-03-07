import sys
import socket
import selectors
import types


HOST = "10.10.10.223"  # Standard loopback interface address (localhost)
PORT = 65433  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print(data.decode())
            sendData = input("N :")
            conn.send(sendData.encode())
            if not data:
                break
            conn.sendall(data)
