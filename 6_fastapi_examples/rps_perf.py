from threading import Thread
import requests

import time


n = 0


def monitor():
    global n
    while True:
        time.sleep(1)
        print(n, 'reqs/sec')
        n = 0


if __name__ == '__main__':
    Thread(target=monitor).start()

    while True:
        requests.get("http://127.0.0.1:8000/fib/1")
        n += 1
