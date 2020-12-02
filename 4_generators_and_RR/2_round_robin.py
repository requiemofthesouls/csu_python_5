def gen(s):
    if type(s) == str:
        for i in s:
            yield i
    elif type(s) == int:
        for i in range(s):
            yield i


def main():
    s = "python"
    g1 = gen(s)
    g2 = gen(len(s))

    tasks = [g1, g2]

    while tasks:
        task = tasks.pop(0)

        try:
            i = next(task)
            print(i)
            tasks.append(task)
        except StopIteration:
            pass


if __name__ == '__main__':
    main()
