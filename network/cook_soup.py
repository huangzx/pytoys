#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
from bs4 import BeautifulSoup
from fetcher import fetcher

VERSION = '0.1'


class CookSoup(object):
    '''

    '''
    def __init__(self):
        pass
    
    def cook(self, url):
        respon = fetcher(url)
        soup = BeautifulSoup(respon)
        return soup


def main():
    '''

    '''
    if len(sys.argv) < 2:
        sys.exit("Provide url")
    url = sys.argv[1]
    cook_soup = CookSoup()
    soup = cook_soup.cook(url)
    print soup.prettify(encoding='utf-8')


if __name__ == '__main__':
    main()
