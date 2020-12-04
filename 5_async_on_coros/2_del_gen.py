from typing import Generator

"""
    Часто возникает ситуация при которой необходимо вызвать из генератора другой генератор
    или из функции другую функцию.
    Делегирующий генератор - это генератор который вызывает другой генератор
    Подгенератор - это вызываемый генератор
"""


def init_gen(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


def subgen():
    """ Читающий генератор """
    for i in "string":
        yield i


def delegator(sg: Generator):
    """ Транслятор """
    for i in sg:
        yield i


sg = subgen()
g = delegator(sg)

print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))
print(next(g))
try:
    print(next(g))
except StopIteration:
    pass

# =====================================
print("=" * 100)


# =====================================

# Теперь переделаем эти генераторы в корутины


@init_gen
def subgen():
    """ Читающий генератор """
    while True:
        try:
            message = yield
        except StopIteration:
            print("StopIteration throwed...")
            break
        else:
            print(f"Received message: {message}")
    return "Returned from subgen()"


@init_gen
def delegator(sg: Generator):
    """ Транслятор """
    while True:
        try:
            data = yield
            sg.send(data)
        except StopIteration as err:
            sg.throw(err)


sg = subgen()
g = delegator(sg)

g.send('test')
g.send('message')
g.send('hello world')
print("Stopping delegator")
g.throw(StopIteration)

"""
@coroutine
def delegator(sg: Generator):
    result = yield from sg  # await
    print(result)
"""

"""
Строго говоря yield from просто yield'ит результат с любого итерируемого объекта
def a():
    yield from "string"
"""
