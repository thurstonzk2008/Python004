def my_map(func, iterable):
    for i in iterable:
        yield func(i)
