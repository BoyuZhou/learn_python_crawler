# coding:utf-8

import re
import urlparse
import urllib2
import time
from datetime import datetime
import robotparser
import Queue


def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, headers=None, user_agent='wswp',
                 proxy=None, num_retries=1, scrape_callback=None):
    """Crawl from the given seed URL following links matched by link_regex
    """
    # 记录被爬过的url队列
    crawl_queue = Queue.deque([seed_url])
    # 记录url被看过且记录深度
    seen = {seed_url: 0}
    # 记录下来了多少个url
    num_urls = 0
    rp = get_robots(seed_url)
    throttle = Throttle(delay)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent

    while crawl_queue:
        url = crawl_queue.pop()
        # 检查网址通过robots.txt限制
        if rp.can_fetch(user_agent, url):
            throttle.wait(url)
            html = download(url, headers, proxy=proxy, num_retries=num_retries)
            links = []
            if scrape_callback:
                links.extend(scrape_callback(url, html) or [])
            depth = seen[url]
            if depth != max_depth:
                # 不达到最大深度，可进行进一步爬取
                if link_regex:
                    # 过滤器，用于与我们的正则表达式匹配的链接
                    links.extend(link for link in get_links(html) if re.match(link_regex, link))

                for link in links:
                    link = normalize(seed_url, link)
                    # 检查是否已抓取此链接
                    if link not in seen:
                        seen[link] = depth + 1
                        # 校验当前url是否是同一域名
                        if same_domain(seed_url, link):
                            # 成功，添加链接到队列中
                            crawl_queue.append(link)

            # 检查是否已达到下载最大值
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print 'Blocked by robots.txt:', url


class Throttle:
    """Throttle downloading by sleeping between requests to same domain
    """

    def __init__(self, delay):
        # 每个域的下载之间的延迟量
        self.delay = delay
        # 何时上次访问域的时间戳
        self.domains = {}

    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()


def download(url, headers, proxy, num_retries, data=None):
    print 'Downloading:', url
    request = urllib2.Request(url, data, headers)
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        response = opener.open(request)
        html = response.read()
        code = response.code
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = ''
        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500 <= code < 600:
                # retry 5XX HTTP errors
                return download(url, headers, proxy, num_retries - 1, data)
        else:
            code = None
    return html


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urlparse.urldefrag(link)  # remove hash to avoid duplicates
    return urlparse.urljoin(seed_url, link)


def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc


def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


def get_links(html):
    """Return a list of links from html 
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, user_agent='BadCrawler')
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, max_depth=1,
                 user_agent='GoodCrawler')