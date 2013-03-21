#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import argparse
from bs4 import BeautifulSoup
from getUrlResponse import getUrlResponse

VERSION = '0.1'


def cookSoup(url):
    respon = getUrlResponse(url)
    soup = BeautifulSoup(respon)
    return soup


def do_search(pkg):
    ''' search archlinux packages

    Args:
      pkg: A string, pkgname

    '''
    # 获得页数, 默认为 1
    pageNum = 1
    url = 'https://www.archlinux.org/packages/?q={}'.format(pkg)
    soup = cookSoup(url)
    if DEBUG:
        sys.stderr.write(soup.prettify(encoding='utf-8'))
    try:
        pkglist = soup.find(attrs={'class': 'pkglist-stats'}).p.text
    except AttributeError:   
        sys.stderr.write("'{}' not found at Arch Packages.\n".format(pkg))
        return 1
    print(pkglist + '\n')
    if 'Page' in pkglist:
        # 原始数据是：'144 packages found. Page 1 of 2.'
        pageNum = int(pkglist.split()[-1].rstrip('.'))
    # 逐页输出搜索到的软件包信息
    print('Arch    Repo    Name    Version    Description    Last Updated\n')
    for num in range(1, pageNum + 1):
        if num > 1:
            url = 'https://www.archlinux.org/packages/?page={}&q={}'.format(num, pkg)
            soup = cookSoup(url)
        find_pkg = []
        find_suburl = []
        for x in soup.find_all('td'):
            find_pkg.append(x.text)
            if x.a:
                find_suburl.append(x.a['href'])
        for x in find_pkg:
            if x == '':
                print('\n')
                continue
            print('{:<6}'.format(x)),
    # 获得 PKGBUILD 等文件的内容
    print '\n'
    find_suburl = list(set(find_suburl))
    for suburl in find_suburl:
        # /packages/community/i686/fcitx-ui-light/ 
        arch = suburl.split('/')[3]
        pkg = suburl.split('/')[4]
        pkgUrl = 'https://www.archlinux.org' + suburl
        soup = cookSoup(pkgUrl)
        sourceUrl = soup.find(attrs={'title': 'View source files for {}'.format(pkg)})['href']
        basepkg = sourceUrl.split('/')[-1]
        plainUrl = sourceUrl.split('/tree/')[0] + '/plain/' + basepkg + '/trunk/'
        soup = cookSoup(plainUrl)
        for x in soup.find_all('li'):
            fileUrl = x.a['href']
            if not fileUrl.endswith('/'):
                print 'https://projects.archlinux.org' + fileUrl


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
