from abc import ABC


class Singleton:
    _instances = {}

    @classmethod
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonABC(ABC, Singleton):
    pass
