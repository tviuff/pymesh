"""Main module for trying out code ideas
"""

import time

import gdfgen as gdf

def main():
    """Function executed if file is executed and not imported"""

def time_it(func):
    """Wrapper function used to time function execution time"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Exceution of '{func.__name__}' took {round((end - start) * 1000)} mil sec.")
        return result
    return wrapper

if __name__ == "__main__":
    main()
