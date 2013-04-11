#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 检查（所返回的）cookie_jar中，是否所有的cookie都存在
# 因为成功登录某网页后，一般都会有对应的cookie返回，所以常用此函数去判断是否成功登录某网页。
# 

def check_all_cookies_exist(cookie_name_list, cookie_jar):
    cookies_dict = {}
    for each_cookie_name in cookie_name_list:
        cookies_dict[each_cookie_name] = False
    all_cookie_found = True
    for cookie in cookie_jar:
        if (cookie.name in cookies_dict):
            cookies_dict[cookie.name] = True
    for each_cookie in cookies_dict.keys():
        if (not cookies_dict[each_cookie]):
            all_cookie_found = False
            break
    return all_cookie_found


if __name__ == '__main__':
    # http://www.darlingtree.com/wordpress/archives/242
    g_val['cj'] = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(g_val['cj']))
    urllib2.install_opener(opener)
    resp = urllib2.urlopen(baidu_space_entry_url);
    login_baidu_url = "https://passport.baidu.com/?login";
    # username=%D0%C4%C7%E9%C6%DC%CF%A2%B5%D8&password=xxx&mem_pass=on
    post_dict = {
        'username'  : username,
        'password'  : password,
        'mem_pass'  : 'on',
    };
    resp = fetcher(login_baidu_url, post_dict)
    # check whether the cookie is OK
    cookie_name_list = ["USERID", "PTOKEN", "STOKEN"]
    login_ok = check_all_cookies_exist(cookie_name_list, g_val['cj'])
    if (not login_ok):
        logging.error("Login fail for not all expected cookies exist!")
        return login_ok
