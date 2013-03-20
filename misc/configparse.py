#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 用 ConfigParser 读写配置文件
#

import ConfigParser


class CaseSConfigParser(ConfigParser.ConfigParser):
    def optionxform(self, optionstr):
        ''' 支持大小写敏感'''
        return optionstr


def main(infile):
    cf = CaseSConfigParser()
    cf.read(infile)
    
    # print sections
    s = cf.sections()    
    print 'sections:', s
    
    # print options of section
    o = cf.options('daemon')
    print 'options:', o
    
    # print value of option 
    v = cf.items('daemon')    
    print 'daemon:', v    
    
    # print value of option using get method
    s = cf.get('daemon', 'AutomaticLoginEnable')
    print s 
    
    # modifiy value of option and write back
    cf.set("daemon", 'AutomaticLoginEnable', 'True') 
    cf.set("daemon", 'AutomaticLogin', 'UserName') 
    cf.write(open(infile, 'w'))   
    

if __name__ == '__main__':
    main('/etc/gdm/custom.conf')
