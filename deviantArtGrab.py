# author: arition
# license: MIT
# contain code from https://github.com/Blux/deviantart-crawler

import requests
from bs4 import BeautifulSoup
import os
import sys

s = requests.Session()
s.cookies = requests.utils.cookiejar_from_dict(dict(agegate_state='1'))


def get_detail_pages(source):
    soup = BeautifulSoup(source, 'html.parser')
    links = []
    for link in soup.find_all('a', class_='t'):
        links.append(link.get('href'))
    return links


def get_image(source):
    soup = BeautifulSoup(source, 'html.parser')
    links = []
    for link in soup.find_all('a', class_='dev-page-download'):
        links.append(link.get('href'))
    return links


def get_pages_count(source):
    soup = BeautifulSoup(source, 'html.parser')
    last_page_link = ''
    max = 0
    for link in soup.find_all('a', attrs={'name': 'gmi-GPageButton', 'class': 'away'}, limit=3):
        offset = int(link.get('data-offset'))
        if offset > max:
            max = offset
    return max / 24


def get_file_name(url):
    index = url.rfind('/')
    indexEnd = url.rfind('?')
    return url[index + 1:indexEnd]


def download_file(url, filename):
    r = s.get(url, stream=True)
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(2048):
            fd.write(chunk)

try:
    username = sys.argv[1]
except:
    print('\nUsage: python %s username\n' % sys.argv[0])
    exit()

url = 'http://%s.deviantart.com/gallery/' % username

# Create dir for user
dirname = username
if not os.path.exists(dirname):
    os.makedirs(dirname)


page_count = get_pages_count(s.get(url).text)
i = 0
print('page count = ' + str(page_count + 1))

while i <= page_count:
    offset = i * 24
    myurl = url + '?offset=' + str(offset)

    myhtml = s.get(myurl).text
    mylinks = get_detail_pages(myhtml)

    print('=============== Getting Page ' + str(i + 1) + ' ===============')

    for link in mylinks:
        myimage_page = s.get(link).text
        myimage = get_image(myimage_page)

        for image in myimage:
            filename = get_file_name(image)
            print('Getting ' + filename)
            download_file(image, dirname + '/' + filename)

    print('Done with page %s\n' % str(i + 1))
    i += 1
print('done with all pages, enjoy!')
