import socket
import selectors

SELECTOR = selectors.DefaultSelector()


def init_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 8000))
    server_socket.listen()

    SELECTOR.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket: socket.socket):
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    SELECTOR.register(fileobj=client_socket, events=selectors.EVENT_READ, data=send_message)


def send_message(client_socket: socket.socket):
    request: bytes = client_socket.recv(4096)
    if request:
        client_socket.send(request)
    else:
        SELECTOR.unregister(client_socket)
        client_socket.close()


def event_loop():
    while True:
        events = SELECTOR.select()  # (key, events) SelectorKey = namedtuple('SelectorKey', ['fileobj', 'fd', 'events', 'data'])

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    init_server()
    event_loop()
