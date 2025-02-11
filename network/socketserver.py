# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 17:29:35 2012

@author: zheng
"""
import socket
import sys
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
s.listen(10)
print 'Socket now listening'
 
conn, addr = s.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call

     
    data = conn.recv(1024)
    reply = 'OK...' + data
    print "client: ", data
    if not data:
        break
     
    conn.sendall(reply)
 
conn.close()
