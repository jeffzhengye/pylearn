# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 15:53:02 2012

@author: zheng
"""

import sys
import socket

a =''
print(a + "a+")

class IPC(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("localhost", 32000))
        self.fid = self.s.makefile() # file wrapper to read lines
        self.listenLoop() # wait listening for updates from server

    def listenLoop(self):
        fid = self.fid
        print "connected"
        while True:
            while True:
                line = fid.readline()
                if line[0]=='.':
                    break
            fid.write('.\n')
            fid.flush()

if __name__ == '__main__':
    st = IPC()