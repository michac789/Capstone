
def f(**kwargs):
    print(kwargs)
    print(kwargs["a"])


f(a = 1, b = 2, c = 3)

