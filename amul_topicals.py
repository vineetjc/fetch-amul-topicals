#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://www.amul.com'

def get_year_urls(page):
    "Gets URLs of all years for which topicals are available"
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table')
    anchors = table.findAll('a')
    urls = {}
    for anchor in anchors:
        if anchor.text != '': # ignore img links
            urls[anchor.text[-4:]] = anchor['href']
    return urls

def fetch_url(url):
    "Fetches the page with the given URL and returns the body"
    r = requests.get(url)
    return r.content

if __name__ == "__main__":
    page = fetch_url(BASE_URL + '/m/amul-hits')
    year_urls = get_year_urls(page)
