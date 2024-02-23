import socket

def send_data_to_server(host, port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.sendall(message.encode())

    data = client_socket.recv(1024)
    print(f"Echoed data: {data.decode()}")

    client_socket.close()

if __name__ == "__main__":
    # Set the host and port for the echo server
    server_host = "10.10.14.230"  # Change this to the IP address of your server
    server_port = 61000

    # Message to be echoed
    message = "Hello, Echo Server!"

    send_data_to_server(server_host, server_port, message)
