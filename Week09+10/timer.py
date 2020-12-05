import time


def timer(func):
    def inner(*args, **kwargs):
        starttime = time.time()
        func(*args, **kwargs)
        endtime = time.time()
        print(f"args:{args},kwargs:{kwargs},func:{func.__name__} spend time:{endtime - starttime}")

    return inner


@timer
def function1(*args, **kwargs):
    time.sleep(1)


if __name__ == "__main__":
    function1(1, {'a': 1}, d=5, f=6)
