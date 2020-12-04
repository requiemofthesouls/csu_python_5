import socket
from select import select
from typing import Generator, Dict, Tuple, List

TO_READ: Dict[socket.socket, Generator] = {}
TO_WRITE: Dict[socket.socket, Generator] = {}
TASKS: List[Generator] = []


def fib(n: int) -> int:
    if n <= 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def server() -> Generator[Tuple[str, socket.socket], None, None]:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 8000))
    server_socket.listen()
    print(f"run server on 8000")

    while True:
        yield "read", server_socket
        client_socket, addr = server_socket.accept()  # read
        print(f"Connection from {addr}")
        TASKS.append(client(client_socket))


def client(client_socket) -> Generator[Tuple[str, socket.socket], None, None]:
    while True:
        yield "read", client_socket
        request = client_socket.recv(4096)  # read

        if not request:
            break
        else:
            result = fib(int(request.decode().strip()))
            response = f"{result}\n".encode()
            yield "write", client_socket
            client_socket.send(response)  # write

    client_socket.close()


def event_loop():
    while any([TASKS, TO_READ, TO_WRITE]):  # False if empty
        while not TASKS:
            ready_to_read, ready_to_write, _ = select(TO_READ, TO_WRITE, [])

            for sock in ready_to_read:
                TASKS.append(TO_READ.pop(sock))

            for sock in ready_to_write:
                TASKS.append(TO_WRITE.pop(sock))

        try:
            task: Generator = TASKS.pop(0)
            reason, sock = next(task)

            if reason == "read":
                TO_READ[sock] = task

            if reason == "write":
                TO_WRITE[sock] = task

        except StopIteration:
            print("Done")


if __name__ == '__main__':
    TASKS.append(server())
    event_loop()
