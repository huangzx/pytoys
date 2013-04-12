#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Zhongxin Huang <zhongxin.huang@gmail.com>
#

import sys
import os
import argparse
import time
from threading import Thread, Lock
from Queue import Queue
from cook_soup import CookSoup
from download_file import download_file

VERSION = '0.1'
SAVEDIR = FETCH = STRICT = VERBOSE = False


def what_time_now():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


class MTDownload(object):
    ''' 多线程下载多个文件
    
    '''
    def __init__(self, threads):
        self.threads = threads
        self.lock = Lock()
        # 任务队列
        self.q_job = Queue()
        # 已完成任务队列
        self.q_done = Queue()
        for i in range(threads):
            t = Thread(target=self.download)
            t.daemon = True
            t.start()
        self.running = 0

    def __del__(self):
        self.q_job.join()
        self.q_done.join()
    
    def task_left(self):
        return self.q_job.qsize() + self.q_done.qsize() + self.running
    
    def push(self, jobs):
        for job in jobs:
            self.q_job.put(job)
    
    def pop(self):
        return self.q_done.get()

    def download(self):
        '''
        '''
        while True:
            job = self.q_job.get()
            if self.lock:
                self.running += 1
            try:
                if VERBOSE:
                    # job[0] - url
                    # job[1] - file to save
                    res = download_file(job[0], job[1], needs_report=True)
                else:
                    res = download_file(job[0], job[1], needs_report=False)
            except Exception:
                pass
            self.q_done.put((job, res))
            if self.lock:
                self.running -= 1
            self.q_job.task_done()
            print(job[1])


def do_search(given_name):
    ''' search and download Arch Linux package database

    Args:
      given_name: A string, pkgname

    '''
    cook_soup = CookSoup()

    # 获得页数, 默认为 1
    page_num = 1
    url = 'https://www.archlinux.org/packages/?q={}'.format(given_name)
    
    if VERBOSE:
        print('Verbose: {} start fetch {}'.format(what_time_now(), url))
    soup = cook_soup.cook(url)
    if VERBOSE:
        print('Verbose: {} finished'.format(what_time_now()))
    
    try:
        pkglist = soup.find(attrs={'class': 'pkglist-stats'}).p.text
    except AttributeError:
        sys.stderr.write("'{}' not found at Arch Packages.\n".format(given_name))
        return 1
    
    print(pkglist + '\n')
    if 'Page' in pkglist:
        # 原始数据是：'144 packages found. Page 1 of 2.'
        page_num = int(pkglist.split()[-1].rstrip('.'))
    #
    # 输出软件包信息
    #
    print('Arch    Repo    Name    Version    Description    Last Updated   Flag Date\n')
    for num in range(1, page_num + 1):
        if num > 1:
            url = 'https://www.archlinux.org/packages/?page={}&q={}'.format(num, given_name)
            if VERBOSE:
                print('Verbose: {} start fetch {}'.format(what_time_now(), url))
            soup = cook_soup.cook(url)
            if VERBOSE:
                print('Verbose: {} finished'.format(what_time_now()))
        found_pkg = []
        found_sub_url = []
        for x in soup.find_all('td'):
            found_pkg.append(x.text)
            if x.a:
                ret = x.a['href']
                if not ret in found_sub_url:
                    found_sub_url.append(ret)
        # 每 7 行换行
        for n in xrange(7, len(found_pkg)+7, 7):
            print ' '.join(found_pkg[n-7:n]),
            print '\n'
    #
    # 获得 PKGBUILD 等文件
    #
    if not FETCH:
        return
    
    found_source_url = []
    for sub_url in found_sub_url:
        #arch = sub_url.split('/')[3]
        name = sub_url.split('/')[4]
        pkg_url = 'https://www.archlinux.org' + sub_url
        
        if VERBOSE:
            print('Verbose: {} start fetch {}'.format(what_time_now(), pkg_url))
        soup = cook_soup.cook(pkg_url)
        if VERBOSE:
            print('Verbose: {} finished'.format(what_time_now()))
        
        source_url = soup.find(attrs={'title': 'View source files for {}'.format(name)})['href']
        if not source_url in found_source_url:
            found_source_url.append(source_url)
            basepkg = source_url.split('/')[-1]
            
            # 如果要求严格匹配软件包名
            if STRICT and (basepkg != given_name):
                continue
            
            # 如果指定了下载目录
            path_to_save = '/tmp'
            if SAVEDIR:
                path_to_save = os.path.realpath(SAVEDIR)
            path_to_save = os.path.join(path_to_save, basepkg)
            if not os.path.exists(path_to_save):
                os.makedirs(path_to_save)
            os.chdir(path_to_save)
            
            plain_url = source_url.split('/tree/')[0] + '/plain/' + basepkg + '/trunk/'
            print "Fetching from {}".format(plain_url)
            
            if VERBOSE:
                print('Verbose: {} start fetch {}'.format(what_time_now(), plain_url))
            soup = cook_soup.cook(plain_url)
            if VERBOSE:
                print('Verbose: {} finished'.format(what_time_now()))
            
            file_urls = []
            for x in soup.find_all('li'):
                file_url = x.a['href']
                if not file_url.endswith('/'):
                    # 每一个文件的真实 URL
                    file_url = 'https://projects.archlinux.org' + file_url
                    if not file_url in file_urls:
                        file_save = file_url.split('/')[-1]
                        file_urls.append((file_url, file_save))
            
            files_num = len(file_urls)
            print 'Download {} files to {}'.format(files_num, path_to_save)
            # 多线程下载, 每个文件一个线程
            mtd = MTDownload(threads=len(file_urls))
            # 将所有任务放入队列
            mtd.push(file_urls)
            while mtd.task_left():
                # 将已完成任务移出队列
                mtd.pop()
            
            print('\n')
            if STRICT and (basepkg == given_name):
                    break


def main():
    argvs = sys.argv[1:]
    if not argvs:
        argvs = ['-h']
    
    desc = 'Search package in Arch Linux, a.k.a https://www.archlinux.org/packages.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-V', '--version', action='store_true', dest='V', 
                        help='show the version number and exit')
    parser.add_argument('-v', '--verbose', action='store_true', dest='v', 
                        help='enable verbose mode')
    parser.add_argument('-f', '--fetch', action='store_true', dest='f', 
                        help='download PKGBUILD and other related files')
    parser.add_argument('-s', '--restrict', action='store_true', dest='s', 
                        help='download match the package name restrictly')
    parser.add_argument('-d', '--dir', nargs=1, metavar='dir', dest='d', 
                        help="download directory, defaults to '/tmp'")
    parser.add_argument('pkg', nargs='*', help='search query')
    args = parser.parse_args(argvs)
    
    if args.V:
        print(VERSION)
    
    if args.v:
        global VERBOSE
        VERBOSE = True

    if args.f:
        global FETCH
        FETCH = True
        if args.d:
            global SAVEDIR
            SAVEDIR = args.d[0]
        if args.s:
            global STRICT
            STRICT = True
    
    if args.pkg:
        for x in args.pkg:
            do_search(x)


if __name__ == '__main__':
    main()
