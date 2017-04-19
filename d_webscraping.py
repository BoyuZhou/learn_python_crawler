# coding:utf-8

import download
import itertools

max_errors = 5

num_errors = 0

for page in itertools.count(1):
    url = 'http://example.webscraping.com/view/%d' % page
    html = download.download(url)
    if html is None:
        num_errors += 1
        if num_errors == max_errors:
            break
        else:
            num_errors = 0

