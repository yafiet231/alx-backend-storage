#!/usr/bin/env python3
"""
main.py - Test script for web.py
"""

from web import get_page

if __name__ == "__main__":
    url = 'http://slowwly.robertomurray.co.uk'
    print(get_page(url))
    print(get_page(url))
    print(get_page(url))
