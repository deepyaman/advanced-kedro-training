from functools import wraps
from typing import Callable


def apply_f(func: Callable) -> Callable:
    @wraps(func)
    def with_f(*args, **kwargs):
        print(*["f({})".format(a) for a in args], **kwargs)
        return func(*args, **kwargs)

    return with_f
