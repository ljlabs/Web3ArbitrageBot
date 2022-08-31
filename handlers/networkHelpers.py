from time import sleep


def infinite_retry(sleep_time):
    def decorator(function):
        def wrapper(*args, **kwargs):
            while True:
                try:
                    return function(*args, **kwargs)
                except:
                    sleep(sleep_time)
        return wrapper
    return decorator


@infinite_retry(1)
def test():
    return "hello"


if __name__ == '__main__':
    print(test())
