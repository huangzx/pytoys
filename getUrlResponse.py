#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 获得 URL 地址的响应
#
# get response from url
# note: if you have already used cookiejar, then here will automatically use it
# while using rllib2.Request
#

import urllib
import urllib2

def getUrlResponse(url, postDict={}, headerDict={}, timeout=0, useGzip=False):
    # makesure url is string, not unicode, otherwise urllib2.urlopen will error
    url = str(url)
    if (postDict):
        postData = urllib.urlencode(postDict)
        req = urllib2.Request(url, postData)
        req.add_header('Content-Type', "application/x-www-form-urlencoded")
    else:
        req = urllib2.Request(url)
    if (headerDict):
        for key in headerDict.keys():
            req.add_header(key, headerDict[key])
    defHeaderDict = {
        'User-Agent'    : ['userAgentIE9'],
        'Cache-Control' : 'no-cache',
        'Accept'        : '*/*',
        'Connection'    : 'Keep-Alive',
    }
    # add default headers firstly
    for eachDefHd in defHeaderDict.keys():
        req.add_header(eachDefHd, defHeaderDict[eachDefHd])
    if (useGzip):
        req.add_header('Accept-Encoding', 'gzip, deflate')
    # add customized header later -> allow overwrite default header 
    if (headerDict):
        for key in headerDict.keys() :
            req.add_header(key, headerDict[key])
    if (timeout > 0):
        # set timeout value if necessary
        resp = urllib2.urlopen(req, timeout=timeout)
    else:
        resp = urllib2.urlopen(req);
    return resp;


if __name__ == '__main__':
    url = 'http://163.com'
    postDict = {}
    headerDict = {}
    timeout = 0
    useGzip = False
    resp = getUrlResponse(url, postDict, headerDict, timeout, useGzip)
    respHtml = resp.read()
    print respHtml
