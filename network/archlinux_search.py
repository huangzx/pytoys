#!/usr/bin/env python
# -*- utf-8 -*-
#

import sys
from bs4 import BeautifulSoup
from getUrlResponse import getUrlResponse
import argparse

__version__ = '0.1'

def do_search(pkg):
    ''' search archlinux packages

    Args:
      pkg: A string, pkgname

    '''
    url = 'https://www.archlinux.org/packages/?q={}'.format(pkg)
    respon = getUrlResponse(url)
    soup = BeautifulSoup(respon)
    if _debug_:
        sys.stderr.write(soup.prettify(encoding='utf-8'))
    print(soup.find(attrs={'class': 'pkglist-stats'}).p.text) + '\n'
    find_pkg = []
    for x in soup.find_all('td'):
        find_pkg.append(x.text)    
        #if x.a:
        #    find_pkg.append(x.a['href'])
    print('Arch    Repo    Name    Version    Description    Last Updated\n')
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
        print(__version__)
    _debug_ = False
    if args.d:
        _debug_ = True
    if args.s:
        for pkg in args.s:
            do_search(pkg)
