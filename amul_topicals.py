#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

HOST = 'http://www.amul.com'
BASE_URL = HOST + '/m/amul-hits'

def get_img_urls(year_page):
    "Gets image URLs of all topicals in the given page"
    soup = BeautifulSoup(year_page, 'html.parser')
    htable = soup.find('table')
    heading = htable.find('strong').text
    print
    print heading
    print "================="
    table = htable.findNext('table')
    anchors = table.findAll('a')
    img_urls = {}
    for anchor in anchors:
        print 'Caption: ' + anchor['title']
        print 'URL: ' + HOST + anchor['href']
        print 'Alt: ' + anchor.find('img')['alt']
        print
        # img_urls[anchor.find('img')['src'][-8:]] = anchor['href']
    # print img_urls

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
    page = fetch_url(BASE_URL)
    year_urls = get_year_urls(page)
    # print year_urls
    for name, url in year_urls.iteritems():
        year_page = fetch_url(BASE_URL + url)
        img_urls = get_img_urls(year_page)
