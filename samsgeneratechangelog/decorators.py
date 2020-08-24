from functools import update_wrapper
import logging

class DebugOutput:

    def __init__(self, func):
        self.func = func
        update_wrapper(self, func)
    
    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        logging.debug(f"Returned {len(result)} values from {self.func.__name__}")
        return result