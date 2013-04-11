#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
from bs4 import BeautifulSoup
from fetcher import fetcher

VERSION = '0.1'


def cook_soup(url):
    '''

    '''
    respon = fetcher(url)
    soup = BeautifulSoup(respon)
    return soup


def main():
    '''

    '''
    if len(sys.argv) < 2:
        sys.exit("Provide url")
    url = sys.argv[1]
    soup = cook_soup(url)
    print soup.prettify(encoding='utf-8')


if __name__ == '__main__':
    main()
