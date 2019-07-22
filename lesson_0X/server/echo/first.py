from functools import reduce

a = [1, 2, 3]


def fer():
    return reduce(lambda x, y: x + [x[-1] + y], a, [0])


if __name__ == '__main__':
    print(fer())
