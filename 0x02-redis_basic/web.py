#!/usr/bin/env python3
"""
In this task, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of
the function is very simple. It uses the requests module
to obtain the HTML content of a particular URL and returns it.

Start in a new file named web.py and do not reuse the code
written in exercise.py.

Inside get_page track how many times a particular URL was
accessed in the key "count:{url}" and cache the result with
an expiration time of 10 seconds.

Tip: Use http://slowwly.robertomurray.co.uk to simulate
a slow response and test your caching.
"""

import redis
import requests
from functools import wraps

# Connect to Redis
r = redis.Redis()

def url_access_count(method):
    """Decorator for get_page function"""
    @wraps(method)
    def wrapper(url):
        """Wrapper function"""
        key = "cached:" + url
        key_count = "count:" + url

        # Increment the access count
        r.incr(key_count)

        # Check if the URL is in the cache
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

        # Get new content and update cache
        html_content = method(url)
        r.setex(key, 10, html_content)
        return html_content
    return wrapper

@url_access_count
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL"""
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    url = 'https://postman-echo.com/delay/3'
    print(get_page(url))
    print(get_page(url))
    print(get_page(url))
