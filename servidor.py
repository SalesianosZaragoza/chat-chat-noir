import socket
import selectors
import sys
import threading
import time

def accept_connection(server_socket, selector):
    client_socket, address = server_socket.accept()
    print(f"Connected to {address}")

    # Recibe el nombre de usuario del cliente
    username = client_socket.recv(1024).decode()
    print(f"Username of client {address}: {username}")

    # Configura el socket del cliente para lectura
    client_socket.setblocking(False)
    selector.register(client_socket, selectors.EVENT_READ, data=username)

def handle_client(client_socket, mask, username, server_socket, selector):
    if mask & selectors.EVENT_READ:
        message = client_socket.recv(1024)
        if message:
            print(f"Received from {username}: {message.decode()}")

            # Envía el mensaje a todos los clientes
            for key in selector.get_map().values():
                if key.fileobj != server_socket and key.data != username:
                    key.fileobj.sendall(f"{username}: {message.decode()}".encode())
        else:
            print(f"Connection with {username} closed")
            selector.unregister(client_socket)
            client_socket.close()

def server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    selector = selectors.DefaultSelector()
    server_socket.setblocking(False)
    selector.register(server_socket, selectors.EVENT_READ)

    try:
        while True:
            events = selector.select()
            for key, mask in events:
                if key.fileobj == server_socket:
                    accept_connection(server_socket, selector)
                else:
                    handle_client(key.fileobj, mask, key.data, server_socket, selector)
    except KeyboardInterrupt:
        print("Server shutting down...")
        selector.unregister(server_socket)
        server_socket.close()

    time.sleep(30)  # Espera 30 segundos antes de salir

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python server.py <host> <port>")
        sys.exit(1)
    
    host, port = sys.argv[1], int(sys.argv[2])
    server(host, port)
