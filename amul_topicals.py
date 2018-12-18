#!/usr/bin/env python
import json, requests, os, sys
from builtins import input
from bs4 import BeautifulSoup
if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve

HOST = 'http://www.amul.com'
BASE_URL = HOST + '/m/amul-hits'

#current working directory
CWD=os.getcwd()

def get_year_topicals(year_page,location):
    "Gets image URLs of all topicals in the given page"
    topicals = {}
    i = 0
    j = 0

    #ask user if they wish to download images by year
    soup = BeautifulSoup(year_page, 'html.parser')
    htable = soup.find('table')
    heading = htable.find('strong').text
    choice = get_user_choice("Do you wish to download images of - "+heading+"?", ['y','n'])
    if choice=='y':
        location = make_folder_in_directory(location,heading)
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
                    if choice=='y':
                        filename= location + "/"+topicals[i]['url'].split('/')[-1]
                        if os.path.exists(filename):
                            print(filename+ ' already exists')
                        else:
                            print(filename)
                            urlretrieve(topicals[i]['url'], filename)
                    i = i + 1
                print
                print (heading + ' page %d successfully accessed.' %(j+1)) #prints if the page was successfully accessed
                print
            except: #after last page; i.e. next page is empty
                return topicals
            j = j + 1

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

def get_user_choice(message, options):
    """User Interaction: Input string message and list of options, returns user choice"""
    choice = input(message + " ("+"/".join(map(str,options))+") :").lower()
    while choice.lower() not in options:
        choice=get_user_choice(message, options)
    return choice

def make_folder_in_directory(location,foldername):
    """Make new folder called <foldername> in the given location; returns the directory of folder"""
    location=location.rstrip('/') #removing any slashes at the end if user has put it
    location=location.rstrip("\\")
    if not os.path.exists(location+"/"+foldername):
        print ("A folder called " + "'" +foldername+"'"+" has been created in "+location)
        os.makedirs(location+"/"+foldername) #slash is provided here
    else:
        print ("Folder "+ "'"+foldername+"'"+" is already present in "+location+"; proceeding to next step...")
    print
    location = location + "/" + foldername
    return location #since modification above; also because folder is to be accessed in the next step

def open_folder(location):
    """Opens the folder at the location; works only for Windows, Mac, Linux"""
    platforms=['win32','linux2','darwin']
    current_platform=sys.platform
    if current_platform not in platforms:
        return
    query = get_user_choice("Do you wish to view the folder?", ['y','n'])
    if query=='y':
        #linux
        if current_platform=='linux2':
            os.system('xdg-open "%s"' % location)
        #mac
        elif current_platform=='darwin':
            os.system('open "%s"' % location)
        #windows
        elif current_platform=='win32':
            os.startfile(location)
        return


if __name__ == "__main__":
    page = fetch_url(BASE_URL)
    year_urls = get_year_urls(page)
    # print year_urls
    print
    d = {}

    #asking user to enter location to save files
    choice = get_user_choice("Save images in current working directory? (a new folder will be created in current directory)", ['y','n'])
    if choice.lower() == 'y':
        location = CWD #storing images in current working directory (default)
    elif choice.lower() == 'n':
        #asking user for entering directory
        location = input("Enter a directory to save images (a new folder will be created in the directory mentioned):")
        while not os.path.isdir(location):
            location = input("Not a valid directory, please enter again:")
    #make new folder called 'Amul Topicals' in the directory; files will be stored in this folder
    location = make_folder_in_directory(location, 'Amul Topicals')

    for name, url in sorted(year_urls.items()):
        year_page = fetch_url(BASE_URL + url)
        per_year = get_year_topicals(year_page,location)
        d[url[3:]] = per_year
    json_data = json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '))
    #print json_data

    #if user wants to view folder right away
    open_folder(location)
