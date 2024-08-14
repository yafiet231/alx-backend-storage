import requests
import redis
import time
from requests.exceptions import RequestException

# Connect to Redis
cache = redis.Redis(host='localhost', port=6379, db=0)

def get_page(url: str) -> str:
    try:
        # Check if the URL is cached
        cached_page = cache.get(url)
        if cached_page:
            # Increment the access count
            cache.incr(f"count:{url}")
            return cached_page.decode('utf-8')
        
        # Fetch the page content
        response = requests.get(url)
        page_content = response.text
        
        # Cache the result with an expiration time of 10 seconds
        cache.setex(url, 10, page_content)
        
        # Initialize the access count
        cache.set(f"count:{url}", 1)
        
        return page_content
    except RequestException as e:
        return f"Error fetching the page: {e}"

# Test the function
if __name__ == "__main__":
    test_url = ("http://slowwly.robertomurray.co.uk/delay/3000/url/"
                "http://www.google.com")
    print(get_page(test_url))
    time.sleep(5)
    print(get_page(test_url))
    time.sleep(6)
    print(get_page(test_url))
