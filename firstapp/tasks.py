from TestProject.celery import myapp


@myapp.task
def supper_sum(x, y):
    return x + y


def divisor(x, y):
    return x / y


def fn1():
    return {'a': 1, 'b': 2}
