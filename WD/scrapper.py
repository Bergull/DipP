# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 16:47:12 2020

@author: Martin
"""

import os
import urllib.request
import json
from urllib.parse import urlparse
import os
os.chdir("K:\DP\WD")

jsonlist = []
#with open("K:/imgs_vids_unfurnished_None_eda39a3ee_e_02_02..json") as fp:
with open ("K:/imgs_vids_floorplan_None_eda39a3ee_e_02_02..json") as fp:
    for jsonObj in fp:
        jsonDict = json.loads(jsonObj)
        jsonlist.append(jsonDict)
jsonlist[2]["item_download_url"]     
urllib.request.urlretrieve(jsonlist[1]["item_download_url"] , "K:/data/flickr/file.jpg")

from urllib.error import URLError
def download_img(url, itemid, savepath):
    if not os.path.exists(join(savepath, "")):
        os.mkdir(join(savepath, ""))
    print(url)
    
    try:
        urllib.request.urlretrieve(url, savepath + str(itemid) + ".jpg")
    except URLError:
        print("not found " + url)
    
for item in jsonlist:
    download_img(item["item_download_url"], item["item_server_identifier"], "K:/data/flickr100mFloorPlan/")
    
    
    
from bs4 import BeautifulSoup
import requests    

html = requests.get("https://www.flickr.com/search/?text=unfurnished&license=1%2C2%2C9%2C10&view_all=1")

soup = BeautifulSoup(html.content)    
imgs = soup.findAll("div", {"class" : "photo-list-photo-view"})
for img in imgs:
    #print(img.get("style"))
    style = img.get("style")
    split = style.split(":")
    #url sixth position
    split[6]
    sliced = split[6][5:][:-1]
    sliced
    download_img("https:" + sliced, split[6][-28:-5], "K:/data/scrape/")

#style = imgs[0].get("style")
#split = style.split(":")
#split[6]
#sliced = split[6][5:][:-1]
#sliced

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time 

# Your options may be different
options = Options()
options.set_preference('permissions.default.image', 2)
options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)


def scroll(driver, timeout):
    scroll_pause_time = timeout
    cookiesbtn = driver.find_elements_by_class_name("primary")
    if len(cookiesbtn) == 0:
            print("no button")
    else:
        driver.execute_script("document.getElementsByClassName('primary')[0].click()")
        print("click")    
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height
        #button = driver.find_element_by_class_name("alt")
        #button.click()
        elems = driver.find_elements_by_class_name("more-res")
        if len(elems) == 0:
            print("no button")
        else:
            time.sleep(scroll_pause_time)
            last_height = driver.execute_script("return document.body.scrollHeight")
            #elems[0].click() 
            driver.execute_script("document.getElementsByClassName('more-res')[0].click()")
            print("click")
        #if(elems.isEmpty())

def get_imgurls(url):
    #yahoo accept cookies
    
    # Setup the driver. This one uses firefox with some options and a path to the geckodriver
    driver = webdriver.Firefox(options=options ,executable_path='K:/geckodriver.exe')
    # implicitly_wait tells the driver to wait before throwing an exception
    
    # driver.get(url) opens the page
    driver.get(url)
    # This starts the scrolling by passing the driver and a timeout
    scroll(driver, 5)
    # Once scroll returns bs4 parsers the page_source
    soup_a = BeautifulSoup(driver.page_source, 'lxml')
    # Them we close the driver as soup_a is storing the page source
    driver.close()

    # Empty array to store the links
    links = []
    imglist = []
    imgs = soup_a.findAll("img")
    #mgs = soup_a.findAll("img", {"class" : "rg-i"})
    for img in imgs:
        #print(img.get("style"))
        imgsrc = img.get("src")
        #styleurl = style.split("url(\"",1)[1]
        #url sixth position
        #split[5]
        #sliced = split[5][5:][:-1]
        #print(sliced)
        if(urlparse(imgsrc)):
            print(imgsrc)
            imglist.append(imgsrc)
    # Looping through all the a elements in the page source
    #for link in soup_a.find_all('a'):
        # link.get('href') gets the href/url out of the a element
        #links.append(link.get('href'))

    return imglist
#allimages = all_links("https://www.flickr.com/search/?text=unfurnished&license=1%2C2%2C9%2C10&view_all=1")
allimages = get_imgurls("https://images.search.yahoo.com/search/images;_ylt=AwrExlRlRYdeEhoAvSuJzbkF?p=floor+plan&fr=yfp-t&imgl=fsu&fr2=p%3As%2Cv%3Ai")
#allimages[2].split(".com/",1)[1][5:-7]

import hashlib 
for file in allimages:
    #print(file(.split(".com/",1)[1][5:-7]))
    #download_img("https:" + file[:-2], file.split(".com/",1)[1][5:-7], "K:/data/scrape/") flickr
    if(str(file) != "None"):
        print(hashlib.md5(str(file).encode('utf-8')).hexdigest())
        download_img(file, hashlib.md5(str(file).encode('utf-8')).hexdigest(), "K:/data/yahooscrape/")




import urllib.request, json 
with urllib.request.urlopen("https://commons.wikimedia.org/w/api.php?action=query&format=json&list=allimages&aiprefix=floor_plan&ailimit=500") as url:
    data = json.loads(url.read().decode())
    data["query"]["allimages"][0]
    for result in data["query"]["allimages"]:
        print(result["url"])
import time
    



    