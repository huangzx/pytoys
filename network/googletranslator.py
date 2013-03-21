#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import urllib
import urllib2
import argparse
from HTMLParser import HTMLParser

VERSION = '0.1'


class HtmlParser(HTMLParser):
    ''' HTML 解析
    
    找到 Google 翻译的结果
    
    '''
    def handle_data(self, data):
        ''' 处理文本元素 '''
        HTMLParser.handle_data(self, data)
        for line in data.split(';'):
            (key, _, value) = line.partition('=')
            if key == 'TRANSLATED_TEXT':
                print value
                break
    def close(self):
        HTMLParser.close(self)


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
    htmlparser= HtmlParser()
    htmlparser.feed(response.read())
    htmlparser.close()


if __name__ == '__main__':
    argvs = sys.argv[1:]
    if not argvs:
        argvs = ['-h']
    desc = 'Google translator, defaults to zh-CN -> en'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-v', '--version', action='store_true',
                        dest='v', help='show version')
    parser.add_argument('-r', '--reverse', action='store_true',
                        dest='r', help='reverse default langpair, a.k.s zh-CN -> en')
    parser.add_argument('-f', '--from', nargs=1, metavar='string',
                        default='en', dest='f', help='source language')
    parser.add_argument('-t', '--to', nargs=1, metavar='string',
                        default='zh-CN', dest='t', help='target language')
    parser.add_argument('string', nargs='*', help='given string')
    args = parser.parse_args(argvs)
    if args.v:
        print VERSION
    if args.r:
        args.f = ['zh-CN']
        args.t = ['en']
    for x in args.string:
        translate(x, args.f[0], args.t[0])
