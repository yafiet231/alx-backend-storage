import requests
import redis
from functools import wraps
from typing import Callable

# Initialize Redis client
redis_client = redis.Redis()

def cache_with_expiration(expiration: int):
    """Decorator to cache the result of a function with an expiration time."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Check if the URL is already cached
            cached_content = redis_client.get(url)
            if cached_content:
                return cached_content.decode('utf-8')
            
            # Call the original function and cache the result
            result = func(url)
            redis_client.setex(url, expiration, result)
            return result
        return wrapper
    return decorator

def track_access_count(func: Callable) -> Callable:
    """Decorator to track the number of times a URL is accessed."""
    @wraps(func)
    def wrapper(url: str) -> str:
        # Increment the access count for the URL
        redis_client.incr(f"count:{url}")
        return func(url)
    return wrapper

@cache_with_expiration(10)
@track_access_count
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL and returns it."""
    response = requests.get(url)
    return response.text
