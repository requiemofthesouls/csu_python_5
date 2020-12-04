from inspect import getgeneratorstate

"""
Корутины (или сопрограммы) это генераторы которые в процессе своей работы
 могут принимать извне какие-то данные (с помощью метода send()),
впринципе генераторы из прошлого примера можно было переделать в корутины

"""


def subgen():
    """
    При инициализации неявно отдаёт None
    При следующем вызове записывается переданное значение в переменную message

    """
    message = yield
    print(f"Subgen received: {message}")


print("Builing subgen generator")
g = subgen()
print(getgeneratorstate(g))
print("Sending None")
g.send(None)  # Инициализация генератора (можно использовать next(g))
print(getgeneratorstate(g))

try:
    g.send("Ok")
except StopIteration:
    pass

# ==================================================
print("=" * 100)


# ==================================================


def subgen2():
    init = "Ready to accept message"
    message = yield init
    print(f"Subgen2 received: {message}")


print("Builing subgen2 generator")
g = subgen2()
print(getgeneratorstate(g))
print("Sending None")
print(next(g))
print(getgeneratorstate(g))
try:
    g.send("Ok")
except StopIteration:
    pass

# ==================================================
print("=" * 100)


# ==================================================


class TestException(Exception):
    pass


def average():
    count, summ, avg = 0, 0, None

    while True:
        try:
            x = yield avg
        except StopIteration:
            print("StopIteration throwed...")
            break
        except TestException:
            print("TestException throwed...")
            break
        else:
            count += 1
            summ += x
            avg = round(summ / count)


print("Builing average generator")
g = average()
print(getgeneratorstate(g))
print("Sending None")
print(next(g))
print(getgeneratorstate(g))
print(g.send(3))
print(g.send(7))
print(g.send(1))
print(g.send(7))
print(g.send(12))
try:
    g.throw(StopIteration)
    # g.throw(TestException)
except StopIteration:
    pass

# ==================================================
print("=" * 100)


# ==================================================


def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


@coroutine
def average():
    count, summ, avg = 0, 0, None

    while True:
        try:
            x = yield avg
        except StopIteration:
            print("StopIteration throwed...")
            break
        except TestException:
            print("TestException throwed...")
            break
        else:
            count += 1
            summ += x
            avg = round(summ / count)

    return avg  # Результат выполнения корутины


print("Building average coroutine")
g = average()
print(getgeneratorstate(g))
print(g.send(5))
print(g.send(3))
print(g.send(9))

try:
    g.throw(StopIteration)
except StopIteration as err:
    print(f"Coroutine done, average: {err.value}")
