import asyncio

"""
asyncio - фреймворк для событийного программирования

Event Loop:
    coroutine <- Task(Future) 
    
asyncio берёт на себя реализацию событийного цикла,
сама создаёт экземпляры класса Task, планирует их выполение.
Нам остаётся реализовать только корутины.
"""


@asyncio.coroutine
def print_nums():
    num = 1
    while True:
        print(num)
        num += 1
        yield from asyncio.sleep(1)


@asyncio.coroutine
def print_time():
    count = 0
    while True:
        if count % 3 == 0:
            print(f"{count} seconds have passed")
        count += 1
        yield from asyncio.sleep(1)


@asyncio.coroutine
def main():
    task1 = asyncio.ensure_future(print_time())  # Важно передавать со скобками, т.к. функция ожидает объект генератора
    task2 = asyncio.ensure_future(print_nums())

    yield from asyncio.gather(task1, task2)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
