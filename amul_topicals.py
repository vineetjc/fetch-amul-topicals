#!/usr/bin/env python
import json
import requests
from bs4 import BeautifulSoup

HOST = 'http://www.amul.com'
BASE_URL = HOST + '/m/amul-hits'

def get_year_topicals(year_page):
    "Gets image URLs of all topicals in the given page"
    topicals = {}
    i = 0
    j = 0
    while True:
        try:
            year_page = fetch_url(BASE_URL + url + '&l='+str(j)) #next 10 records
            soup = BeautifulSoup(year_page, 'html.parser')
            htable = soup.find('table')
            heading = htable.find('strong').text
            # print "================="
            table = htable.findNext('table')
            anchors = table.findAll('a')
            for anchor in anchors:
                topicals[i] = {
                    'caption': anchor['title'],
                    'url': HOST + anchor['href'],
                    'alt': anchor.find('img')['alt']
                }
                i = i + 1
            print heading + ' page %d' %(j+1) #prints if the page was successfully accessed
            print
        except: #after last page; i.e. next page is empty
            return topicals
        j+=1

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
    print
    d = {}
    for name, url in year_urls.iteritems():
        year_page = fetch_url(BASE_URL + url)
        per_year = get_year_topicals(year_page)
        d[url[3:]] = per_year
    json_data = json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '))
    print json_data
