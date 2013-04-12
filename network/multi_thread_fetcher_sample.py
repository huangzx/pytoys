#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Multi Thread Class
#

import sys
from threading import Thread
from Queue import Queue
from bs4 import BeautifulSoup
from fetcher import fetcher
from cook_soup import CookSoup


class Scheduler(object):
    '''

    Args:
      work: func, working function
      num: int, working thread number
      jobs: interator, jobs

    '''
    def __init__(self, work, num, jobs):
        self.work = work
        self.num = num
        self.jobs = jobs

    def worker(self):
        while True:
            job = self.q.get()
            self.work(job)
            self.q.task_done()
    
    def run(self):
        self.q = Queue()
        
        for i in range(self.num):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()
        
        for job in self.jobs:
            self.q.put(job)
        
        self.q.join()


class MyCookSoup(CookSoup):
    '''

    '''
    def cook(self, url):
        respon = fetcher(url)
        soup = BeautifulSoup(respon)
        print 'Done', url
        return soup


def main():
    urls = (
        'http://www.phoronix.com/scan.php?page=news_item&px=MTM0OTQ',
        'http://www.phoronix.com/scan.php?page=news_item&px=MTM0OTM',
        'http://www.phoronix.com/scan.php?page=news_item&px=MTM0OTI',
        'http://www.phoronix.com/scan.php?page=news_item&px=MTM0OTE',
        'http://www.phoronix.com/scan.php?page=news_item&px=MTM0OTA',
        'http://www.phoronix.com/scan.php?page=news_item&px=MTM0ODk',
        'http://www.phoronix.com/scan.php?page=news_item&px=MTM0ODg',
        'http://www.phoronix.com/scan.php?page=news_item&px=MTM0ODY',
        'http://www.phoronix.com/scan.php?page=news_item&px=MTM0ODY'
        )

    my_cook_soup = MyCookSoup()
    scheduler = Scheduler(my_cook_soup.cook, len(urls), urls)
    scheduler.run()


if __name__ == '__main__':
    main()
