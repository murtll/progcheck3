import functools

def log(*args, **kwargs):
    """Used to log some messages"""
    message = kwargs['message']

    def decorate(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            print(message.format(args[0].name, args[1], args[0].health - args[1] if args[0].health - args[1] > 0 else 0))

            to_execute = fn(*args, **kwargs)
        return wrapper
    return decorate

class UnknownSpeedException(Exception):
    def __init__(self):
        super().__init__('unknown speed')

class UnknownDistanceException(Exception):
    def __init__(self):
        super().__init__('unknown distance')

class UnknownReloadException(Exception):
    def __init__(self):
        super().__init__('unknown reload')
