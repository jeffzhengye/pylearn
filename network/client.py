# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 17:57:32 2012

@author: zheng
"""

import socket

sket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sket.connect(('localhost', 32000))

sket.send('send')


a = ''
a.lo
