#!/usr/bin/env python
# -*- utf-8 -*-
#

from bs4 import BeautifulSoup
from getUrlResponse import getUrlResponse
import sys

def do_search(pkg):
    ''' search archlinux packages

    Args:
      pkg: A string, pkgname

    '''
    url = 'https://www.archlinux.org/packages/?q={}'.format(pkg)
    respon = getUrlResponse(url)
    soup = BeautifulSoup(respon)
    #print soup.prettify(encoding='utf-8')
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
    for pkg in sys.argv[1:]:
        do_search(pkg)
