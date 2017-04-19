# coding:utf-8
# 限速类

import urlparse
import datetime
import time

class Throttle:
    """Add a delay between downloads to the same domain"""

    def __init__(self, delay):
        self.delay = delay

        self.domain = {}

    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)s


        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)

        self.domains[domain] = datetime.datetime.now()