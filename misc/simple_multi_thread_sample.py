#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 多线程一个简单的例子
# 效率提升，仅供参考：
# 4 线程：
# ./simple_multi_thread.py  0.04s user 0.00s system 0% cpu 12.548 total
# 1 线程：
# ./simple_multi_thread.py  0.03s user 0.01s system 0% cpu 50.092 total
#
#

from threading import Thread
from Queue import Queue
from time import sleep


def do_work(i):
    ''' 实际工作函数 '''
    print('完成: {}'.format(i))

def worker():
    ''' 工人，负责不断从队列取数据并处理 '''
    while True:
        item = q.get()
        do_work(item)
        sleep(0.5)
        q.task_done()

q = Queue()

# N 个并发线程
for i in range(4):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

print 'Start'

# 共 N 个任务, 放到队列里
for i in range(100):
    q.put(i)

# 等待所有任务
q.join()

print 'Done'
