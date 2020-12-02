from time import time


def gen_symbol(s):
    for i in s:
        yield i


def gen_filename():
    while True:
        t = int(time() * 1000)

        print("before yield")
        yield f"file-{t}.jpeg"

        print("after yield")


def many_yields():
    yield 1
    yield 2
    yield 3


# Run in interactive mode python3 -i 1_generators.py
gs = gen_symbol("python")
gf = gen_filename()
gm = many_yields()
