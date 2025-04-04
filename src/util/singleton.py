import abc
from threading import Lock

class Singleton(abc.ABCMeta,type):
    _instances = {}
    _lock = Lock()
    #
    def __call__(cls, *args, **kwargs):
        """call method for singleton metaclass"""
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton,cls).__call__(*args,**kwargs)
            return cls._instances[cls]