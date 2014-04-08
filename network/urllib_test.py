__author__ = 'zheng'

import urllib



def testDownload():
    url = "http://www.ozdic.com/collocation-dictionary/handy"
    f = urllib.urlopen(url)
    content = f.read()
    print content
    f.close()


def batch_down_from_ozdic():
    import time
    counter = 0
    baseurl = 'http://www.ozdic.com/collocation-dictionary/'
    with open('/home/zheng/Dropbox/workspace/sigir14/word2vec-read-only/pyword2vec_revise/disk1_5.txt') as fsource:
        for line in fsource:
            for word in line.split():
                url = baseurl + word
                f = urllib.urlopen(url)
                content = f.read()
                #print content
                f.close()
                counter += 1
                print 'downloading %s-th page' % counter
                time.sleep(8)


batch_down_from_ozdic()

