import sys

result_map = dict(a=None, b=None)


def f(num):
    if num == 0:
        return 1

    if num == 1:
        return 2

    a = f(num - 1)
    b = f(num - 2)

    if result_map["a"] is None:
        result_map["a"] = a

    if result_map["b"] is None:
        result_map["b"] = b

    return result_map["a"] * result_map["b"]


if __name__ == "__main__":
    result = f(0)
    print(result)

    result = f(1)
    print(result)

    result = f(2)
    print(result)

    result = f(12)
    print(result)
