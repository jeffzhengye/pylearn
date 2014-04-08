__author__ = 'zheng'

# coding: UTF-8

from bs4 import BeautifulSoup
import urllib2
import sys


# Obtain keyword from shell command
def obtain_keyword():
    try:
        return sys.argv[1]
    except:
        print 'ERROR: yd(youdao) takes one parameter.'
        sys.exit()


# Obtain option from shell command
def obtain_option():
    try:
        option = sys.argv[2]
        if option != '-s':
            print 'ERROR: option should be used as "yd keyword -s"'
            sys.exit()
        return option
    except:
        pass


# Crawl youdao dic page and return a bs4.BeautifulSoup object
def crawl_page(keyword):
    url = 'http://dict.youdao.com/search?le=eng&q=%s&keyfrom=dict.index' % keyword
    # use try to check network connection
    try:
        page = urllib2.urlopen(url).read()
    except:
        print 'ERROR: network connection failed.'
        sys.exit()
    soup = BeautifulSoup(page)
    return soup


# Find the basic definition
def basic_definition(soup):
    s1 = soup.find(id='phrsListTab')

    basic_def = []
    lst = []
    try:
        lst = s1.find_all('li')
    except:
        pass
    for l in lst:
        if l.string:
            basic_def.append(l.string)
    return basic_def

def collins(soup):
	sp = soup.find(id='collinsResult')
	return sp

# find definition of the 21st century big english-chinese dictionary
def century_21_definition(soup):
    s2 = soup.find(id='authDictTrans')
    century_21 = []
    part_of_speech = s2.ul.children
    for p in part_of_speech:
        try:
            if p.ul:
                li = p.ul.find_all('li')
                for l in li:
                    if l:
                        definition = l.span.string
                        example = l.find_all('p')
                        sentences = [e.string for e in example]
                        century_21.append([definition, sentences])
        except AttributeError:
            pass
    return century_21


# print basic definition
def print_basic_definition(basic_def):
    print '*****************************************************************'
    for b in basic_def:
        print b
    print '*****************************************************************'


# print definition of the 21st century big english-chinese dictionary
def print_century_21_definition(century_21):
    i = 0
    for c in century_21:
        i += 1
        print i,
        print c[0]
        for q in c[1]:
            print '    ',  # four blank space
            print q
    print '*****************************************************************'


def main():
    #keyword = obtain_keyword()
    keyword = 'make'
    soup = crawl_page(keyword)
    print collins(soup)
    import sys
    sys.exit(1)
    basic_def = basic_definition(soup)
    if not basic_def:
        print "No such word, please try again!"
        return
    print_basic_definition(basic_def)
    specific = obtain_option()
    if specific:
        century_21 = century_21_definition(soup)
        print_century_21_definition(century_21)


if __name__ == '__main__':
    main()
    # import cProfile
    # cProfile.run('main()')