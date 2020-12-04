import requests
import time

if __name__ == '__main__':
    while True:
        start = time.time()
        res = requests.get("http://127.0.0.1:8000/fib/30")
        end = time.time()
        print(round(end - start, 5))
