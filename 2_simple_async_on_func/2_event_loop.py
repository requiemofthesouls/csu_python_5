import socket
from select import select


def fib(n):
    if n <= 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


TO_MONITOR = []


def accept_connection(server_socket: socket.socket):
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    TO_MONITOR.append(client_socket)


def send_message(client_socket: socket.socket):
    request: bytes = client_socket.recv(4096)
    if request:
        n = int(request)
        result = fib(n)
        client_socket.send(f"{result}\n".encode())
    else:
        TO_MONITOR.remove(client_socket)
        print(f"Lost connection")
        client_socket.close()


def event_loop():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 8000))
    server_socket.listen()

    TO_MONITOR.append(server_socket)

    while True:
        ready_to_read, ready_to_write, erors = select(TO_MONITOR, [], [])

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    event_loop()
