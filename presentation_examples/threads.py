import time
import threading

start = time.perf_counter()


def please_sleep(n):
    print(f"Sleeping for {n} seconds")
    time.sleep(n)
    print(f"Done Sleeping for {n} seconds")


threads = []

for i in range(1, 6):
    t = threading.Thread(target=please_sleep, args=(i,))
    t.start()
    threads.append(t)
for t in threads:
    t.join()

finish = time.perf_counter()
print(f"Finished in {finish - start} seconds")


