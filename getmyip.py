#!/usr/bin/env python
# -*- utf-8 -*-

import re
import urllib2

class Getmyip:
    '''

    '''
    def getip(self):
        try:
            myip = self.visit("http://www.ip138.com/ip2city.asp")
        except:
            try:
                myip = self.visit("http://www.bliao.com/ip.phtml")
            except:
                try:
                    myip = self.visit("http://www.whereismyip.com/")
                except:
                    myip = "So sorry!!!"
        return myip
    
    def visit(self, url):
        opener = urllib2.urlopen(url)
        if url == opener.geturl():
            str = opener.read()
        return re.search('\d+\.\d+\.\d+\.\d+',str).group(0)

getmyip = Getmyip()
localip = getmyip.getip()
print localip

#curl icanhazip.com
