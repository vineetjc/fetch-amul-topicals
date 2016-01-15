#!/usr/bin/env python

import requests

def fetch_url(url):
    "Fetches the page with the given URL and returns the body"
    r = requests.get(url)
    return r.content

if __name__ == "__main__":
    print fetch_url("http://www.amul.com/m/amul-hits")
