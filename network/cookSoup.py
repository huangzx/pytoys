#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
from bs4 import BeautifulSoup
from getUrlResponse import getUrlResponse

VERSION = '0.1'


def cookSoup(url):
    respon = getUrlResponse(url)
    soup = BeautifulSoup(respon)
    return soup


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Provide url")
    url = sys.argv[1]
    soup = cookSoup(url)
    print soup.prettify(encoding='utf-8')
