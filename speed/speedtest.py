"""
https://wiki.python.org/moin/PythonSpeed/PerformanceTips
"""
__author__ = 'zheng'


def sortby(somelist, n):
	"""
	Suppose, for example, you have a list of tuples that you want to sort by the n-th field of each tuple.
	"""
	nlist = [(x[n], x) for x in somelist]
	nlist.sort()
	return [val for (key, val) in nlist]

def sortby_inplace(somelist, n):
	"""
	Matching the behavior of the current list sort method (sorting in place) is easily achieved as well:
	"""
	somelist[:] = [(x[n], x) for x in somelist]
	somelist.sort()
	somelist[:] = [val for (key, val) in somelist]
	return

somelist = [(1, 2, 'def'), (2, -4, 'ghi'), (3, 6, 'abc')]
n = 1
import operator
somelist.sort(key=operator.itemgetter(n)) ## this is the fastest way to sort

#####################string concatenation#######################
slist = ['dfasdf', 'dfadfsd', 'dfewesdfsdafd', 'dsafsfdasd']

def cat1(l):
	"""
	%timeit cat1(slist)
10000 loops, best of 3: 49.3 us per loop
	"""
	l = l*100
	s=''
	for sbstr in l:
		s += sbstr
	return s

def cat2(l):
	"""
	%timeit cat2(slist)
10000 loops, best of 3: 23.3 us per loop
	"""
	l = l*100
	slist = [x for x in l]
	return ''.join(slist)

def cat3():
	"""
	1000000 loops, best of 3: 234 ns per loop
	"""
	return "<html>" + 'head' + 'prologue' + 'query' + 'tail' + "</html>"

def cat4():
	"""
	1000000 loops, best of 3: 370 ns per loop
	Note: the results on my laptop conflict with that in https://wiki.python.org/moin/PythonSpeed/PerformanceTips
	"""
	return "<html>%s%s%s%s</html>" % ('head', 'prologue', 'query', 'tail')

########################loops################################

def up1(l, time=100):
	"""
	10000 loops, best of 3: 94.7 us per loop
	"""
	l = l*time
	nlist=[]
	for w in l:
		nlist.append(w.upper())
	return nlist

def up11(l, time=100):
	"""
	Avoiding dots...
	10000 loops, best of 3: 89.2 us per loop
	"""
	l = l*time
	nlist=[]
	upper = str.upper
	append = nlist.append
	for w in l:
		append(upper(w))
	return nlist

def up2(l, time=100):
	"""
	10000 loops, best of 3: 65.4 us per loop
	"""
	l = l*time
	nlist = map(str.upper, l)

def up3(l, time=100):
	"""
	10000 loops, best of 3: 70.5 us per loop
	"""
	l = l*time
	nlist = [s.upper() for s in l]
	return nlist

