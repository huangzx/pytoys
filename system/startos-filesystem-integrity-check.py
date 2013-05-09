#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Author: Zhongxin Huang <zhongxin.huang@gmail.com>
#

import os
import sys
import argparse
import multiprocessing
import ybs.utils, ybs.pybs, ybs.settings
import sqlite3

PROCESSES_NUM = 4
ALL_FILES_RECORD = 'allfiles'
ALL_EXECFILES_RECORD = 'execfiles'
ALL_LINKS_RECORD = 'alllinks'


def is_in_database(infile):
    ''' 
    
    '''
    conn = sqlite3.connect(ybs.settings.__package_db__)
    cur = conn.cursor()
    cur.execute("SELECT distinct * FROM {} WHERE file = '{}'".format('world_file', infile))
    if cur.fetchone() is None:
        return False
    return True
    conn.close()
    cur.close()


def get_not_owned(infile):
    '''
    
    '''
    try:
        if not is_in_database(infile):
            print("'{}' not found in file database".format(infile))
        return infile
    except KeyboardInterrupt:
        raise KeyboardInterruptError()


def get_invalid_link(inlink):
    '''
    '''
    try:
        dest = os.path.realpath(inlink)
        if not os.path.exists(dest):
            print("'{}' link target is not exist".format(inlink)),
            if is_in_database(inlink):
                print("but it is in database")
        return inlink
    except KeyboardInterrupt:
        raise KeyboardInterruptError()


def get_ldd_not_found(infile):
    '''
    
    '''
    try:
        ldd_result = os.popen('ldd '+infile+' '+'2>/dev/null').readlines()
        for line in ldd_result:
            line = line.strip()
            if 'not found' in line:
                print(line)
        return infile
    except KeyboardInterrupt:
        raise KeyboardInterruptError()


def is_skip(line):
    '''

    '''
    skips = ('/locale/', '/core_perl/',
             '/usr/lib/systemd/', '/usr/lib/udev/',
             '/include/', '/usr/lib/grub/',
             '/vendor_perl/') 
    for skip in skips:
        if skip in line:
            return True
    suffixes = ('pyc', 'pyo', 'txt', 'xml', 'docbook',
                'cmake', 'xsl', 'entities',
                'gz', 'h', 'pc', 'qm', 'conf',
                'prf', 'decTest', 'html')
    for suffix in suffixes: 
        if line.endswith('.'+suffix):     
            return True
    return False


def mppoolmap(func, files):
    '''

    '''
    pool = multiprocessing.Pool(PROCESSES_NUM)
    try:
        result = pool.map(func, files)
        pool.close()
    except KeyboardInterrupt:
        pool.terminate()
    finally:    
        pool.join()
    if len(result) != len(files):
        sys.stderr.write('Datas mismatch: found {}, but handled {}\n'.format(len(files), len(result)))
    else:
        print("Handled {} files with multiprocessing".format(len(result)))
    return result


def get_exec(infile):
    '''
    
    '''
    try:
        if not is_skip(infile):
            result = os.popen('file -b '+'"'+infile+'"').readline()
            if 'LSB executable' in result or 'LSB shared object' in result:
                return infile
    except KeyboardInterrupt:
        raise KeyboardInterruptError()


def files_in_dir(indir, type='file'):
    '''

    '''
    for root, dirs, files in os.walk(indir):
        for file_ in files:
            absfile = (os.path.join(root, file_))
            if type == 'file':
                yield absfile
            elif type == 'link':
                if os.path.islink(absfile):
                    yield absfile


def get_all_files(afs):
    '''

    '''
    print("Find all files of filesystem, please wait some minutes...")
    dirs = ('/lib', '/lib64', '/sbin', '/usr')
    afsd = open(afs, 'w')
    for dir_ in dirs:
        for file_ in files_in_dir(dir_):
                afsd.write(file_+'\n')
    afsd.close()
    print("Write to '{}', please see it for details".format(afs))


def get_all_links(als):
    '''

    '''
    print("Find all symlinks of filesystem, please wait some minutes...")
    dirs = ('/bin', '/etc', '/lib', '/lib64', '/opt', '/sbin', '/usr')
    alsd = open(als, 'w')
    for dir_ in dirs:
        for link in files_in_dir(dir_, type='link'):
                alsd.write(link+'\n')
    alsd.close()
    print("Write to '{}', please see it for details".format(als))


def get_all_execfiles(aefs):
    '''

    '''
    print("Find all executable files of filesystem, please wait some minutes...")
    exec_dirs = ('/bin', '/lib', '/lib64', '/sbin', '/usr/bin', '/usr/lib', '/usr/lib64', '/usr/libexec', '/usr/sbin')
    exec_files_raw = []
    for dir_ in exec_dirs:
        for file_ in files_in_dir(dir_):
                exec_files_raw.append(file_)
    result = mppoolmap(get_exec, exec_files_raw)
    aefsd = open(aefs, 'w')
    for file_ in result:
        if file_:
            aefsd.write(file_+'\n')
    aefsd.close()
    print("Write to '{}', please see it for details".format(aefs))


def start(msg=''):
    ''' '''
    print('Start {} at {}'.format(msg, ybs.utils.what_time()))


def stop():
    ''' '''
    print('Finish at {}'.format(ybs.utils.what_time()))


class ISOCheck(object):
    '''

    '''
    def __init__(self):
        ''' '''
        self.conn = sqlite3.connect(ybs.settings.__package_db__)
        self.cur = self.conn.cursor()
        self.pkgs_installed = ybs.pybs.ybs_list_installed()
        self.len_pkgs_installed = len(self.pkgs_installed)
    
    def __del__(self):
        ''' '''
        self.cur.close()
        self.conn.close()

    def isolated_file(self, afs):
        ''' '''
        start('checking for isolated files')
        files_raw = [x.strip() for x in open(afs, 'r').readlines()]
        print('Found {} files'.format(len(files_raw)))
        mppoolmap(get_not_owned, files_raw)
        stop()
    
    def lack_of_lib(self, aefs):
        ''' '''
        start('checking for lack of libraries')
        files_raw = [x.strip() for x in open(aefs, 'r').readlines()]
        print('Found {} executable files'.format(len(files_raw)))
        mppoolmap(get_ldd_not_found, files_raw)
        stop()

    def invalid_link(self, als):
        ''' '''
        start('checking for invalid symlinks')
        links_raw = [x.strip() for x in open(als, 'r').readlines()]
        print('Found {} symlinks'.format(len(links_raw)))
        mppoolmap(get_invalid_link, links_raw)
        stop()
    
    def isolated_pkg(self):
        ''' '''
        start('checking for isolated packages')
        print('{} packages installed'.format(self.len_pkgs_installed))
        for pkg in self.pkgs_installed:
            self.cur.execute("SELECT {} FROM {} WHERE name = '{}'".format('name', 'universe', pkg))
            if self.cur.fetchone() is None:
                print("'{}' not found in universe".format(pkg))
        stop()

    def conflict_pkg(self):
        ''' '''
        start('checking for conflicting packages')
        print('{} packages installed'.format(self.len_pkgs_installed))
        for pkg in self.pkgs_installed:
            self.cur.execute("SELECT {} FROM {} WHERE name = '{}'".format('data_conflict', 'world_data', pkg))
            res = self.cur.fetchone()
            if res is not None and res[0]:
                for cp in res[0].split(','):
                    if cp in self.pkgs_installed:
                        print("'{}' is conflict with '{}',".format(cp, pkg)),
                        print('and it was not installed')
        stop()

    def replace_pkg(self):
        ''' '''
        start('checking for replaceable packages')
        print('{} packages installed'.format(self.len_pkgs_installed))
        for pkg in self.pkgs_installed:
            self.cur.execute("SELECT {} FROM {} WHERE name = '{}'".format('data_replace', 'world_data', pkg))
            res = self.cur.fetchone()
            if res is not None and res[0]:
                for rp in res[0].split(','):
                    if rp in self.pkgs_installed:
                        print("'{}' can be replaced by '{}',".format(rp, pkg)),
                        print('but it was not installed')
        stop()

    def yget_conf(self):
        ''' '''
        with open('/etc/yget.conf', 'r') as file_:
            for line in file_.readlines():
                print line.strip()


def main():
    argvs = sys.argv[1:]
    if not argvs:
        argvs = ['-h']
    
    if '-A' in argvs or '--all' in argvs:
        argvs = ['-g', '-l', '-c', '-of', '-op', '-cp', '-rp']

    desc = 'Check file system before you make ISO'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-A', '--all', action='store_true',
                        dest='A', help="do all the check in one time")
    parser.add_argument('-g', '--all_files', action='store_true',
                        dest='g', help="find all the files and executable files")
    parser.add_argument('-l', '--lack_of_lib', action='store_true',
                        dest='l', help="find the executable files which lack for runtime libraries, by 'ldd'")
    parser.add_argument('-c', '--yget_conf', action='store_true',
                        dest='c', help="show content of '/etc/yget.conf'")
    parser.add_argument('-of', '--isolated_file', action='store_true',
                        dest='of', help="find the isolated files, namely, which are not in file database")
    parser.add_argument('-op', '--isolated_pkg', action='store_true',
                        dest='op', help="find the installed packages which are not in package source")
    parser.add_argument('-cp', '--conflict_pkg', action='store_true',
                        dest='cp', help='find the installed and conflicting packages')
    parser.add_argument('-rp', '--replace_pkg', action='store_true',
                        dest='rp', help='find the installed and replaceable packages')
    parser.add_argument('-il', '--invalid_link', action='store_true',
                        dest='il', help='find invalid symlinks, namely, link target does not exist')
    args = parser.parse_args(argvs)
    
    if args.g:
        get_all_files(ALL_FILES_RECORD)
        get_all_links(ALL_LINKS_RECORD)
        get_all_execfiles(ALL_EXECFILES_RECORD)
    
    isocheck = ISOCheck()
    if args.of:
        if not os.path.isfile(ALL_FILES_RECORD):
            get_all_files(ALL_FILES_RECORD)
        isocheck.isolated_file(ALL_FILES_RECORD)
    
    if args.l:
        if not os.path.isfile(ALL_EXECFILES_RECORD):
            get_all_execfiles(ALL_EXECFILES_RECORD)
        isocheck.lack_of_lib(ALL_EXECFILES_RECORD)
    
    if args.il:
        if not os.path.isfile(ALL_LINKS_RECORD):
            get_all_links(ALL_LINKS_RECORD)
        isocheck.invalid_link(ALL_LINKS_RECORD)    

    if args.op:
        isocheck.isolated_pkg()
    
    if args.cp:
        isocheck.conflict_pkg()
    
    if args.rp:
        isocheck.replace_pkg()
    
    if args.c:
        isocheck.yget_conf()


if __name__ == '__main__':
    main()
