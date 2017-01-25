'''
Created on 2017. 1. 24.

@author: joeylee
'''

import os
import subprocess
import threading

'''
    2016/11/12
    ping test
    using thread pool & run as daemon
'''


class Pinger(object):
    status = {'alive': [], 'dead': []}
    hosts = []

    thread_count = 10

    lock = threading.Lock()

    '''
        return 0 if ping test is successful
    '''
    def ping(self, ip):
        print('ping function start')
        ret = subprocess.call(['ping', '-n', '1', ip],
                              stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))

        return ret == 0

    def pop_queue(self):
        print('pop_queue function start')
        ip = None

        self.lock.acquire()

        if self.hosts:
            ip = self.hosts.pop()

        self.lock.release()
        return ip

    def dequeue(self):
        print('dequeue function start')
        while True:
            ip = self.pop_queue()
            print('ip : ' + ip)

            if not ip:
                return None

            result = 'alive' if self.ping(ip) else 'dead'
            print('result :' + result)
            self.status[result].append(ip)

    '''
        start thread pool
        blocking method
    '''
    def start(self):
        print('start function start')
        threads = []

        for i in range(self.thread_count):
            t = threading.Thread(target=self.dequeue)
            t.setDaemon(True)
            t.start()
            threads.append(t)

        [t.join() for t in threads]

        return self.status
