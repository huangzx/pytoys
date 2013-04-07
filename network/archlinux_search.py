#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Zhongxin Huang <zhongxin.huang@gmail.com>
#

import sys
import os
import argparse
from cook_soup import cook_soup
from download_file import download_file

VERSION = '0.1'


def do_search(given_name):
    ''' search and download Arch Linux package database

    Args:
      given_name: A string, pkgname

    '''
    # 获得页数, 默认为 1
    page_num = 1
    url = 'https://www.archlinux.org/packages/?q={}'.format(given_name)
    soup = cook_soup(url)
    try:
        pkglist = soup.find(attrs={'class': 'pkglist-stats'}).p.text
    except AttributeError:
        sys.stderr.write("'{}' not found at Arch Packages.\n".format(given_name))
        return 1
    print(pkglist + '\n')
    if 'Page' in pkglist:
        # 原始数据是：'144 packages found. Page 1 of 2.'
        page_num = int(pkglist.split()[-1].rstrip('.'))
    #
    # 输出软件包信息
    #
    print('Arch    Repo    Name    Version    Description    Last Updated   Flag Date\n')
    for num in range(1, page_num + 1):
        if num > 1:
            url = 'https://www.archlinux.org/packages/?page={}&q={}'.format(num, given_name)
            soup = cook_soup(url)
        found_pkg = []
        found_sub_url = []
        for x in soup.find_all('td'):
            found_pkg.append(x.text)
            if x.a:
                ret = x.a['href']
                if not ret in found_sub_url:
                    found_sub_url.append(ret)
        # 每 7 行换行
        for n in xrange(7, len(found_pkg)+7, 7):
            print ' '.join(found_pkg[n-7:n]),
            print '\n'
    #
    # 获得 PKGBUILD 等文件
    #
    if not FETCH:
        return
    found_source_url = []
    for sub_url in found_sub_url:
        #arch = sub_url.split('/')[3]
        name = sub_url.split('/')[4]
        pkg_url = 'https://www.archlinux.org' + sub_url
        soup = cook_soup(pkg_url)
        source_url = soup.find(attrs={'title': 'View source files for {}'.format(name)})['href']
        if not source_url in found_source_url:
            found_source_url.append(source_url)
            basepkg = source_url.split('/')[-1]
            # 如果要求严格匹配软件包名
            if STRICT and (basepkg != given_name):
                continue
            # 如果指定了下载目录
            path_to_save = '/tmp'
            if SAVEDIR:
                path_to_save = os.path.realpath(SAVEDIR)
            path_to_save = os.path.join(path_to_save, basepkg)
            if not os.path.exists(path_to_save):
                os.makedirs(path_to_save)
            os.chdir(path_to_save)
            plain_url = source_url.split('/tree/')[0] + '/plain/' + basepkg + '/trunk/'
            print "Fetching from {}".format(plain_url)
            print 'Download to {}'.format(path_to_save)
            soup = cook_soup(plain_url)
            for x in soup.find_all('li'):
                file_url = x.a['href']
                if not file_url.endswith('/'):
                    # 每一个文件的真实 URL
                    file_url = 'https://projects.archlinux.org' + file_url
                    file_save = file_url.split('/')[-1]
                    print 'Get: {}'.format(file_save)
                    download_file(file_url, file_save, needs_report=False)
            print('\n')
            if STRICT and (basepkg == given_name):
                    break


if __name__ == '__main__':
    argvs = sys.argv[1:]
    if not argvs:
        argvs = ['-h']
    
    desc = (
            'Search package in Arch Linux package database, '
            'a.k.a https://www.archlinux.org/packages.'
    )
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
