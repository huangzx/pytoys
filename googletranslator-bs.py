#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import urllib
import urllib2
import argparse
from bs4 import BeautifulSoup

VERSION = '0.1'

def translate(text, source, target):
    ''' Google 翻译
    
    Args:
      text: 待翻译文本
      source: 源语言
      target: 目标语言

    '''
    values = {'hl': target, 'ie': 'utf8', 'text': text, 'langpair': '{}|{}'.format(source, target)}
    url = 'http://translate.google.cn/translate_t'
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)')
    response = urllib2.urlopen(req)
    soup = BeautifulSoup(response)
    result = soup.find(id='result_box').string
    if result:
        print unicode(result)


if __name__ == '__main__':
    argvs = sys.argv[1:]
    if not argvs:
        argvs = ['-h']
    desc = 'Google translator'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-v', '--version', action='store_true',
                        dest='v', help='show version')
    parser.add_argument('-f', '--from', nargs=1, metavar='string',
                        default='en', dest='f', help='source language')
    parser.add_argument('-t', '--to', nargs=1, metavar='string',
                        default='zh-CN', dest='t', help='target language')
    parser.add_argument('string', nargs='*', help='given string')
    args = parser.parse_args(argvs)
    if args.v: 
        print VERSION
    for x in args.string:
        translate(x, args.f[0], args.t[0])
