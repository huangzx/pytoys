#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 检查（所返回的）cookieJar中，是否所有的cookie都存在
# 因为成功登录某网页后，一般都会有对应的cookie返回，所以常用此函数去判断是否成功登录某网页。
# 

def checkAllCookiesExist(cookieNameList, cookieJar):
    cookiesDict = {}
    for eachCookieName in cookieNameList:
        cookiesDict[eachCookieName] = False
    allCookieFound = True
    for cookie in cookieJar:
        if (cookie.name in cookiesDict):
            cookiesDict[cookie.name] = True
    for eachCookie in cookiesDict.keys():
        if (not cookiesDict[eachCookie]):
            allCookieFound = False
            break
    return allCookieFound


if __name__ == '__main__':
    # http://www.darlingtree.com/wordpress/archives/242
    gVal['cj'] = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(gVal['cj']))
    urllib2.install_opener(opener)
    resp = urllib2.urlopen(baiduSpaceEntryUrl);
    loginBaiduUrl = "https://passport.baidu.com/?login";
    #username=%D0%C4%C7%E9%C6%DC%CF%A2%B5%D8&password=xxx&mem_pass=on
    postDict = {
        'username'  : username,
        'password'  : password,
        'mem_pass'  : 'on',
    };
    resp = getUrlResponse(loginBaiduUrl, postDict)
    # check whether the cookie is OK
    cookieNameList = ["USERID", "PTOKEN", "STOKEN"]
    loginOk = checkAllCookiesExist(cookieNameList, gVal['cj'])
    if (not loginOk):
        logging.error("Login fail for not all expected cookies exist!")
        return loginOk
