#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 检查/判断/校验网络上某个文件是否有效
# check file validation:
# open file url to check return info is match or not
# with exception support
# note: should handle while the file url is redirect
# eg:
# http://publish.it168.com/2007/0627/images/500754.jpg ->
# http://img.publish.it168.com/2007/0627/images/500754.jpg
# other special one:
# sina pic url: 
# http://s14.sinaimg.cn/middle/3d55a9b7g9522d474a84d&690
# http://s14.sinaimg.cn/orignal/3d55a9b7g9522d474a84d
# the real url is same with above url
#

import urllib
import urllib2

def is_file_valid(file_url):
    file_is_valid = False
    err_reason = ''

    try:
        orig_file_name = file_url.split('/')[-1]
        low_unquoted_orig_filename = urllib.unquote(orig_file_name).lower()
        resp = urllib2.urlopen(file_url) 
        real_url = resp.geturl()
        new_filename = real_url.split('/')[-1]
        low_unquoted_new_filename = urllib.unquote(new_filename).lower()
        resp_info = resp.info()
        resp_code = resp.getcode()
        # 如果是 http 请求，200 表示请求成功完成; 404 表示网址未找到.
        # 如果是 ftp 请求, 返回 None, 等另外处理
        if (low_unquoted_orig_filename == low_unquoted_new_filename) and (resp_code == 200):
            file_is_valid = True
        else:
            # eg: Content-Type= image/gif, ContentTypes : audio/mpeg
            # more ContentTypes can refer: http://kenya.bokee.com/3200033.html
            content_type = resp_info['Content-Type']
            content_len = resp_info['Content-length']
            err_reason = 'URL returned info: type={}, len={}, real_url={}'.format(content_type, content_len, real_url)
    except urllib2.URLError, reason:
        file_is_valid = False
        err_reason = reason
    except urllib2.HTTPError, code:
        file_is_valid = False
        err_reason = code
    except:
        file_is_valid = False
        err_reason = 'Unknown error'
    
    if err_reason:
        err_reason = str(err_reason)
    return (file_is_valid, err_reason)


if __name__ == '__main__':
    #cur_url = 'http://img2.cache.netease.com/photo/0001/2013-03-19/8QA0UTSV3R710001.jpg'
    cur_url = 'ftp://192.168.1.11/ads/ads.txt'
    (pic_is_valid, err_reason) = is_file_valid(cur_url)
    print pic_is_valid, err_reason
