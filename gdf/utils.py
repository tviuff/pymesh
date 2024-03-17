"""Mdule containing utility functions
"""

import time

def time_it(func):
    """Wrapper function used to time function execution time"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Exceution of '{func.__name__}' took {round((end - start) * 1000)} mil sec.")
        return result
    return wrapper
