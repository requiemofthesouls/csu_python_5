import socket
from threading import Thread
from concurrent.futures import ProcessPoolExecutor as Pool

pool = Pool(4)


def fib(n):
    if n <= 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def run_server(address, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((address, port))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()  # blocking
        print(f"Connection from {addr}")
        handle_client(client_socket)  # synchronus execution
        # Thread(target=handle_client, args=(client_socket,), daemon=True).start()


def handle_client(client_socket: socket.socket):
    while True:
        request: bytes = client_socket.recv(4096)  # blocking

        if not request:
            break
        else:
            n = int(request)
            # future = pool.submit(fib, n)
            # result = future.result()
            result = fib(n)
            client_socket.send()  # blocking

    client_socket.close()


if __name__ == '__main__':
    run_server("", 8000)

"""
Особенности работы с потоками в Python.
1. С GIL Python не может использовать несколько ядер процессора одновременно,
     фактически она привязывает питон к одному ядру. Можно убедиться если запустить несколько скриптов time_perf.py 
     (время обработки запросов будет увеличиваться).
 
2. Если во время выполнения коротких запросов (rps_perf.py) например запросить число 40го ряда
 (послать запрос с тяжелым вычислением) - будет просадка по rps (почти до нуля), т.к. GIL отдаст приоритет на выполнение тяжелой задаче.
 Если запускать тяжелые вычисления в отдельном процессе, то просадка будет минимальной, т.к. приоритет будет за мелкими задачами.
 
3. Можно использовать ProcessPoolExecutor, однако накладные расходы возрастают в разы, можно проверить rps_perf.py. 
   Производительность снизилась, но т.к. вычисления производятся в разных процессах - просадки по rps нет.
   

С помощью потоков мы хотели обойти блокирующие операции. 
Поток (нить) позволяет сгладить блокировки (останавливают выполнение и начинают ждать),
 но в питоне есть функциональность которая останавливают выполнение схожим образом - это функция-генератор, но об этом чуть позже.
"""
