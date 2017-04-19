# coding:utf-8

import download
import re

def crawl_sitemap(url):
    sitemap = download.download(url)
    links = re.findall('<loc>(.*?)</loc>', sitemap)

    for link in links:
        html = download.download(link)


crawl_sitemap('http://example.webscraping.com/sitemap.xml')

