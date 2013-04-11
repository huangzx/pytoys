#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Multi Thread Class
#

from threading import Thread
from Queue import Queue
from time import sleep


class SMTC(object):
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
            sleep(0.5)
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


def foo(i):
    print('done: {}'.format(i))


def main():
    smtc = SMTC(foo, 2, range(10))
    smtc.run()


if __name__ == '__main__':
    main()
