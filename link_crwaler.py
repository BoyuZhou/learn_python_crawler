# coding: utf-8

import re
import download
import urlparse

def link_crawler(seed_url, link_regex, max_depth=2):
    """Crawl from the given seed URL following links matched by link_regex"""
    # 增加深度
    max_depth = 2
    seen = {}
    crawl_queue = [seed_url]



    while crawl_queue:
        url = crawl_queue.pop()
        html = download.download(url)

        depth = seen[url]
        if depth != max_depth:
            for link in get_links(html):
                if re.match(link_regex, link):
                    link = urlparse.urljoin(seed_url, link)
                    if link not in seen:
                        seen[link] = depth + 1
                        crawl_queue.append(link)

def get_links(html):
    """Return a list of links from html"""
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)

link_crawler('http://example.webscraping.com', '/(index|view)')