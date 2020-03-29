# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 20:06:51 2019

@author: Nathan
"""

from bs4 import BeautifulSoup
import requests
import os
import urllib.request
from zipfile import ZipFile

dest = 'C:\\Users\\Jdpre\\Desktop\\Big Data\\Project\\Data\\Users'
os.chdir(dest)

html_page = requests.get('http://netsg.cs.sfu.ca/youtubedata/')
src = html_page.content
soup = BeautifulSoup(src, 'lxml')

links = soup.find_all("a")

'''
2007 NormalCrawl: 4:39
2008 NormalCrawl: 39:98
UpdateCrawl 98:126
FileSize & Bitrate: 126:129
User Information: 129:131
'''


norm07 = links[129:131]
norm07n = [i.attrs['href'] for i in norm07]

for link in norm07n:
    url = 'http://netsg.cs.sfu.ca/youtubedata/' + link
    print("Downloading: " + link)
    urllib.request.urlretrieve(url, link)
    with ZipFile(link, 'r') as zipObj:
        print("\tExtracting: " + link)
        zipObj.extractall()
        zipObj.close()
#    print("\tDeleting: " + link)
    os.remove(link)
    
    
    
    
