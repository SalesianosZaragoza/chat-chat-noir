import socket
import selectors
import sys
import threading
import time

def receive_message(client_socket):
    while True:
        message = client_socket.recv(1024)
        if message:
            print(message.decode())
        else:
            print("Connection closed by server")
            break

def send_message(client_socket):
    while True:
        message = input("msg: ")
        if not message:
            break
        client_socket.sendall(message.encode())

def client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print(f"Connected to server at {host}:{port}")

    # Solicita al usuario que ingrese su nombre de usuario
    username = input("Enter username: ")
    client_socket.sendall(username.encode())

    # Configura el selector para leer y escribir desde/hacia el socket del cliente
    selector = selectors.DefaultSelector()
    selector.register(client_socket, selectors.EVENT_READ)

    # Crea un hilo para recibir mensajes del servidor
    receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
    receive_thread.start()

    # Envía mensajes al servidor
    send_message(client_socket)

    receive_thread.join()  # Espera a que termine el hilo de recepción
    client_socket.close()
    print("Connection with server closed")

    time.sleep(30)  # Espera 30 segundos antes de salir

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <host> <port>")
        sys.exit(1)
    
    host, port = sys.argv[1], int(sys.argv[2])
    client(host, port)
