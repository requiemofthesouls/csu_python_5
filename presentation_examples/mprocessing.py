import time
import multiprocessing

start = time.perf_counter()


def please_sleep(n):
    print(f"Sleeping for {n} seconds")
    time.sleep(n)
    print(f"Done Sleeping for {n} seconds")


processes = []

for i in range(1, 6):
    p = multiprocessing.Process(target=please_sleep, args=(i,))
    p.start()
    processes.append(p)
for p in processes:
    p.join()

finish = time.perf_counter()
print(f"Finished in {finish - start} seconds")


