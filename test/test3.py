from mmlib import check


@check
def f(x: int):
    return x**2

f("1")