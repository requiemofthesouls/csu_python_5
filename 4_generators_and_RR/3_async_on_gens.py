import socket


def client(client_socket):
    while True:
        request = client_socket.recv(4096)  # read

        if not request:
            break
        else:
            client_socket.send(request)  # write
        client_socket.close()


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 8000))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()  # read
        print(f"Connection from {addr}")
        client(client_socket)
