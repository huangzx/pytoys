#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Zhongxin Huang <huangzhongxin@ivali.com>
#

import sys
import urllib
import urllib2


def get_url_response(url, post_dict={}, header_dict={}, timeout=0, use_gzip=False):
    ''' 获得 URL 地址的响应 
    
    Args:
     url: A string
     post_dict: A dict 
     header_dict: A dict
     timeout: A int
     use_gzip: A bool, False or True 
    
    Returns:
      urllib2.urlopen object      

    To use:
     >>>from get_url_response import get_url_response
     >>>respo = get_url_response(url, post_dict={}, header_dict={}, timeout=0, use_gzip=False)
     >>>respohtml = respo.read()
    
    '''
    # Make sure url is string rather than unicode, otherwise urllib2.urlopen occur error
    url = str(url)
    if post_dict:
        post_data = urllib.urlencode(post_dict)
        req = urllib2.Request(url, post_data)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    else:
        req = urllib2.Request(url)
    default_header_dict = {
        'User-Agent': ['userAgentIE9'], 
        'Cache-Control': 'no-cache',
        'Accept': '*/*',
        'Connection': 'Keep-Alive',
    }
    for each_def_hd in default_header_dict.keys():
        req.add_header(each_def_hd, default_header_dict[each_def_hd])
    if use_gzip:
        req.add_header('Accept-Encoding', 'gzip, deflate')
    if header_dict:
        for key in header_dict.keys():
            req.add_header(key, header_dict[key])
    if timeout > 0:
        respon = urllib2.urlopen(req, timeout=timeout)
    else:
        respon = urllib2.urlopen(req);
    return respon


def main():
    '''

    '''
    if len(sys.argv) < 2:
        sys.exit("Provide url")
    url = sys.argv[1]
    respon = get_url_response(url)
    print(respon)


if __name__ == '__main__':
    main()
