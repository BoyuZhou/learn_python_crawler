# coding:utf-8

import requests
import os
from lxml import html
import time
import sys


# 获取主页列表
def getPage():
    baseUrl = 'http://www.mzitu.com/'
    selector = html.fromstring(requests.get(baseUrl).content)

    urls = []
    for i in selector.xpath('//ul[@id="pins"]/li/a/@href'):
        urls.append(i)
    return urls


print 'starting'





# 图片链接列表，标题
# url是详情页链接

def getPiclink(url):
    sel = html.fromstring(requests.get(url).content)

    total = sel.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]

    title = sel.xpath('//h2[@class="main-title"]/text()')[0]

    jpgList = []

    for i in range(int(total)):
        link = '{}/{}'.format(url, i + 1)
        s = html.fromstring(requests.get(link).content)

        jpg = s.xpath('//div[@class="main-image"]/p/a/img/@src')[0]

        jpgList.append(jpg)

    return title, jpgList


def downloadPic((title, piclist)):
    k = 1

    count = len(piclist)

    dirName = u"【%sP】%s" % (str(count), title)

    os.mkdir(dirName)

    for i in piclist:
        filename = '%s/%s/%s.jpg' % (os.path.abspath('.'), dirName, k)

        print u'开始下载图片：%s 第%s张' % (dirName, k)

        with open(filename, "wb") as jpg:
            jpg.write(requests.get(i).content)
            time.sleep(0.5)
        k += 1

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    pageNum = input(u'请输入页码：')
    for link in getPage():
        downloadPic(getPiclink(link))