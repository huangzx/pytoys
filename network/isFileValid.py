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

def isFileValid(fileUrl):
    fileIsValid = False
    errReason = ''

    try:
        origFileName = fileUrl.split('/')[-1]
        lowUnquotedOrigFilename = urllib.unquote(origFileName).lower()
        resp = urllib2.urlopen(fileUrl) 
        realUrl = resp.geturl()
        newFilename = realUrl.split('/')[-1]
        lowUnquotedNewFilename = urllib.unquote(newFilename).lower()
        respInfo = resp.info()
        respCode = resp.getcode()
        # 如果是 http 请求，200 表示请求成功完成; 404 表示网址未找到.
        # 如果是 ftp 请求, 返回 None, 等另外处理
        if (lowUnquotedOrigFilename == lowUnquotedNewFilename) and (respCode == 200):
            fileIsValid = True
        else:
            # eg: Content-Type= image/gif, ContentTypes : audio/mpeg
            # more ContentTypes can refer: http://kenya.bokee.com/3200033.html
            contentType = respInfo['Content-Type']
            contentLen = respInfo['Content-length']
            errReason = 'URL returned info: type={}, len={}, realUrl={}'.format(contentType, contentLen, realUrl)
    except urllib2.URLError, reason:
        fileIsValid = False
        errReason = reason
    except urllib2.HTTPError, code:
        fileIsValid = False
        errReason = code
    except:
        fileIsValid = False
        errReason = 'Unknown error'
    
    if errReason:
        errReason = str(errReason)
    return (fileIsValid, errReason)


if __name__ == '__main__':
    #curUrl = 'http://img2.cache.netease.com/photo/0001/2013-03-19/8QA0UTSV3R710001.jpg'
    curUrl = 'ftp://192.168.1.11/ads/ads.txt'
    (picIsValid, errReason) = isFileValid(curUrl)
    print picIsValid, errReason
