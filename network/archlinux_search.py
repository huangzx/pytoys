#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Zhongxin Huang <zhongxin.huang@gmail.com>
#

import sys
import os
import argparse
from cookSoup import cookSoup
from downloadFile import downloadFile

VERSION = '0.1'


def do_search(givenName):
    ''' search archlinux packages

    Args:
      givenName: A string, pkgname

    '''
    # 获得页数, 默认为 1
    pageNum = 1
    url = 'https://www.archlinux.org/packages/?q={}'.format(givenName)
    soup = cookSoup(url)
    try:
        pkglist = soup.find(attrs={'class': 'pkglist-stats'}).p.text
    except AttributeError:
        sys.stderr.write("'{}' not found at Arch Packages.\n".format(givenName))
        return 1
    print(pkglist + '\n')
    if 'Page' in pkglist:
        # 原始数据是：'144 packages found. Page 1 of 2.'
        pageNum = int(pkglist.split()[-1].rstrip('.'))
    #
    # 输出软件包信息
    #
    print('Arch    Repo    Name    Version    Description    Last Updated   Flag Date\n')
    for num in range(1, pageNum + 1):
        if num > 1:
            url = 'https://www.archlinux.org/packages/?page={}&q={}'.format(num, givenName)
            soup = cookSoup(url)
        find_pkg = []
        find_suburl = []
        for x in soup.find_all('td'):
            find_pkg.append(x.text)
            if x.a:
                ret = x.a['href']
                if not ret in find_suburl:
                    find_suburl.append(ret)
        # 每 7 行换行
        for n in xrange(7, len(find_pkg)+7, 7):
            print ' '.join(find_pkg[n-7:n]),
            print '\n'
    #
    # 获得 PKGBUILD 等文件
    #
    if not FETCH:
        return
    find_sourceurl = []
    for suburl in find_suburl:
        #arch = suburl.split('/')[3]
        name = suburl.split('/')[4]
        pkgUrl = 'https://www.archlinux.org' + suburl
        soup = cookSoup(pkgUrl)
        sourceUrl = soup.find(attrs={'title': 'View source files for {}'.format(name)})['href']
        if not sourceUrl in find_sourceurl:
            find_sourceurl.append(sourceUrl)
            basepkg = sourceUrl.split('/')[-1]
            # 如果要求严格匹配软件包名
            if STRICT and (basepkg != givenName):
                continue
            # 如果指定了下载目录
            pathSave = '/tmp'
            if SAVEDIR:
                pathSave = os.path.realpath(SAVEDIR)
            pathSave = os.path.join(pathSave, basepkg)
            if not os.path.exists(pathSave):
                os.makedirs(pathSave)
            os.chdir(pathSave)
            plainUrl = sourceUrl.split('/tree/')[0] + '/plain/' + basepkg + '/trunk/'
            print "Fetching from {}".format(plainUrl)
            print 'Download to {}'.format(pathSave)
            soup = cookSoup(plainUrl)
            for x in soup.find_all('li'):
                fileUrl = x.a['href']
                if not fileUrl.endswith('/'):
                    # 每一个文件的真实 URL
                    fileUrl = 'https://projects.archlinux.org' + fileUrl
                    fileSave = fileUrl.split('/')[-1]
                    print 'Get: {}'.format(fileSave)
                    downloadFile(fileUrl, fileSave, needReport=False)
            print('\n')
            if STRICT and (basepkg == givenName):
                    break


if __name__ == '__main__':
    argvs = sys.argv[1:]
    if not argvs:
        argvs = ['-h']
    desc = ('Search package in Arch Linux Packages, '
            'a.k.a https://www.archlinux.org/packages.')
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-v', '--version', action='store_true', dest='v', 
                        help='show the version number and exit')
    parser.add_argument('-f', '--fetch', action='store_true', dest='f', 
                        help='download PKGBUILD and other related files')
    parser.add_argument('-s', '--strict', action='store_true', dest='s', 
                        help='download strictly match the package name')
    parser.add_argument('-d', '--dir', nargs=1, metavar='dir', dest='d', 
                        help="download directory, defaults to '/tmp'")
    parser.add_argument('pkg', nargs='*', help='search query')
    args = parser.parse_args(argvs)
    if args.v:
        print(VERSION)
    SAVEDIR = FETCH = STRICT = False
    if args.f:
        FETCH = True
        if args.d:
            SAVEDIR = args.d[0]
        if args.s:
            STRICT = True
    if args.pkg:
        for x in args.pkg:
            do_search(x)
