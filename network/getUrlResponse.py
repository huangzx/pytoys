#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import urllib
import urllib2


def getUrlResponse(url, postDict={}, headerDict={}, timeout=0, useGzip=False):
    ''' 获得 URL 地址的响应 
    
    Args:
     url: A string
     postDict: A dict 
     headerDict: A dict
     timeout: A int
     useGzip: A bool, False or True 
    
    Returns:
      urllib2.urlopen object      

    To use:
     >>>import ybsutils
     >>>respo = getUrlResponse(url, postDict={}, headerDict={}, timeout=0, useGzip=False)
     >>>respohtml = respo.read()
    
    '''
    # makesure url is string, not unicode, otherwise urllib2.urlopen will error
    url = str(url)
    if postDict:
        postData = urllib.urlencode(postDict)
        req = urllib2.Request(url, postData)
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    else:
        req = urllib2.Request(url)
    defHeaderDict = {
        'User-Agent': ['userAgentIE9'], 
        'Cache-Control': 'no-cache',
        'Accept': '*/*',
        'Connection': 'Keep-Alive',
    }
    for eachDefHd in defHeaderDict.keys():
        req.add_header(eachDefHd, defHeaderDict[eachDefHd])
    if useGzip:
        req.add_header('Accept-Encoding', 'gzip, deflate')
    if headerDict:
        for key in headerDict.keys():
            req.add_header(key, headerDict[key])
    if timeout > 0:
        respon = urllib2.urlopen(req, timeout=timeout)
    else:
        respon = urllib2.urlopen(req);
    return respon
