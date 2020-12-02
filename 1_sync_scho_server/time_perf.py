from socket import *
import time

if __name__ == '__main__':
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('localhost', 8000))

    while True:
        start = time.time()
        sock.send(b'30')
        resp = sock.recv(100)
        end = time.time()
        print(end - start)
