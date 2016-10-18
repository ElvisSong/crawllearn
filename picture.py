# coding=utf-8
from bs4 import BeautifulSoup
import urllib2
import time
import os

URL = 'http://gank.io'
headers = {'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36'}

def gethtml(url, num_retries = 2):
    print "Downloading:", url
    request = urllib2.Request(url, headers = headers)
    try:
        html =  urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return gethtml(url, num_retries-1)
    return html

def build_uri(endpoint):
    return URL + endpoint

def get_articleurl(html):
    articleurl=[]
    soup = BeautifulSoup(html,"lxml")
    history = soup.select("li > div > a")
    for his in history:
        article = his.get('href')
        # print article
        articleurl.append(build_uri(article))
    return articleurl

def getpicurl(html):
    soup = BeautifulSoup(html,"lxml")
    # print soup
    url= soup.select("p > img")[0]
    # print url
    srcurl = url.get('src')
    print srcurl
    return srcurl

def downloader(srcurl,name):
    url = urllib2.Request(srcurl,headers = headers)
    f = urllib2.urlopen(url,data=None,timeout=3)
    imgdata = f.read()
    save_img(name.replace('/','-')+".jpg",imgdata)
    print "download:"+ str(name) +".jpg"

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def save_img(file_name, data):
    """if data == None:
        return
    mkdir(path)
    if (not path.endswith("/")):
        path = path+"/"
    """
    fp = os.open(file_name, os.O_CREAT | os.O_RDWR)
    os.write(fp, data)
    os.close(fp)


if __name__ == '__main__':
    mainhtml = gethtml(URL+'/history')
    articleurl = get_articleurl(mainhtml)
    for article in articleurl:
        print article
        time.sleep(2)
        articlehtml = gethtml(article)
        srcurl = getpicurl(articlehtml)
        downloader(srcurl,article[15:])
