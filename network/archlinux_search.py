#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import argparse
from bs4 import BeautifulSoup
from getUrlResponse import getUrlResponse

VERSION = '0.1'


def do_search(pkg):
    ''' search archlinux packages

    Args:
      pkg: A string, pkgname

    '''
    # 获得页数, 默认为 1
    pageNum = 1
    url = 'https://www.archlinux.org/packages/?q={}'.format(pkg)
    respon = getUrlResponse(url)
    soup = BeautifulSoup(respon)
    if DEBUG:
        sys.stderr.write(soup.prettify(encoding='utf-8'))
    pkglist = soup.find(attrs={'class': 'pkglist-stats'}).p.text
    print(pkglist + '\n')
    if 'Page' in pkglist:
        # 原始数据是：'144 packages found. Page 1 of 2.'
        pageNum = int(pkglist.split()[-1].rstrip('.'))
    # 逐页输出
    print('Arch    Repo    Name    Version    Description    Last Updated\n')
    for num in range(1, pageNum + 1):
        if num >= 2:
            url = 'https://www.archlinux.org/packages/?page={}&q={}'.format(num, pkg)
            respon = getUrlResponse(url)
            soup = BeautifulSoup(respon)
        find_pkg = []
        for x in soup.find_all('td'):
            find_pkg.append(x.text)    
            #if x.a:
            #    find_pkg.append(x.a['href'])
        for x in find_pkg:
            if x == '':
                print('\n')
                continue
            print('{:<6}'.format(x)),


if __name__ == '__main__':
    argvs = sys.argv[1:]
    if not argvs:
        argvs = ['-h']
    desc = 'Search package in https://www.archlinux.org/packages.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-v', '--version', action='store_true',
                        dest='v', help='show version')
    parser.add_argument('-d', '--debug', action='store_true',
                        dest='d', help='show debug')
    parser.add_argument('-s', '--search', nargs='*', metavar='pkg',
                        dest='s', help='search pkgname')
    args = parser.parse_args(argvs)
    if args.v:
        print(VERSION)
    DEBUG = False
    if args.d:
        DEBUG = True
    if args.s:
        for pkg in args.s:
            do_search(pkg)
