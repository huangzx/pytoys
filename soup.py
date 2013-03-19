#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 获得 URL 指向地址，返回 html 格式
#

import sys
import urllib2
from bs4 import BeautifulSoup as Soup

def get_url(url):
  data = None
  headers = {'Accept-Language': 'en-us',}
  req = urllib2.Request(url, data, headers)
  u = urllib2.urlopen(req)
  soup = Soup(u)
  print soup.prettify(encoding='utf-8')
  return soup

if __name__ == '__main__':
    if len(sys.argv) < 2:
      sys.exit("Provide url")
    url = sys.argv[1]
    get_url(url)
