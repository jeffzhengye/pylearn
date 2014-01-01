"""
Python implementation of left leaning RBT
https://class.coursera.org/algs4partI-003/lecture/50

Note: doesn't support duplicate values
"""
__author__ = 'zheng'

RED = True
BLACK = False

def isRed(node):
	if node is None: return False
	return node.color == RED


class Node:
	def __init__(self, data=None):
		self.data = data
		self.left = None
		self.right = None
		self.count = 0
		self.color = RED


class LLRBT:
	def __init__(self):
		self.root = None

	def rotateLeft(self, h):
		assert isRed(h.right)
		x = h.right
		h.right = x.left
		x.left = h
		x.color = h.color
		h.color = RED
		return x

	def rotateRight(self, h):
		assert isRed(h.left)
		x = h.left
		h.left = x.right
		x.right = h
		x.color = h.color
		h.color = RED
		return x

	def put(self, data):
		self.root = self._put(self.root, data)

	def _put(self, h, data):
		if h is None: return Node(data)
		if data < h.data:
			h.left = self._put(h.left, data)
		elif data > h.data:
			h.right = self._put(h.right, data)
		else:
			h.data = data
			return h

		if isRed(h.right) and not isRed(h.left):
			h = self.rotateLeft(h)
		if isRed(h.left) and isRed(h.left.left):
			h = self.rotateRight(h)
		if isRed(h.left) and isRed(h.right):
			h = self._flipColors(h)
		return h

	def _flipColors(self, h):
		h.left.color = BLACK
		h.right.color = BLACK
		h.color = RED
		return h

	def search_nonrecursive(self, data):
		proot = self.root
		while proot is not None:
			if data == proot.data:
				return proot
			elif data < proot.data:
				proot = proot.left
			else:
				proot = proot.right
		return None


	def search(self, data):
		return self._search(self.root, data)

	def _search(self, node, data):
		if node is None:
			return None
		if data == node.data:
			return node
		elif data < node.data:
			return self._search(node.left, data)
		else:
			return self._insert(node.right, data)

	def floor(self, data):
		return self._floor(self.root, data)

	def _floor(self, node, data):
		if node is None:
			return None
		if data == node.data:
			return node
		if data < node.data:
			return self._floor(node.left, data)

		t = self._floor(node.righ, data)
		if t is not None:
			return t
		else:
			return node

	def ceiling(self, data):
		return self._ceiling(self.root, data)

	def _ceiling(self, node, data):
		pass

	def rank(self, data):
		return self._rank(self.root, data)

	def _rank(self, node, data):
		if node is None: return 0
		if data < node.data:
			return self._rank(node.left, data)
		elif data > node.data:
			return self.__size__(node.left) + 1 + self._rank(node.right, data)
		else:
			return self.__size__(node.left)

	def delete(self, data):
		"""
		not finished
		"""
		self.root = self.__delete__(self.root, data)

	def __delete__(self, node, data):
		if node is None: return None
		if data < node.data:
			node.left = self.__delete__(node.left, data)
		elif data > node.data:
			node.right = self.__delete__(node.right, data)
		else:
			if node.right is None:
				return node.left
			else:
				t = node
				node = self.__min__(t.right)
				node.right = self.__delMin__(node.right)
				node.left = t.left
		return node


	def min(self):
		return self._min(self.root)

	def _min(self, node):
		if node.left is None:
			return node
		else:
			return self._min(node.left)

	def delMin(self):
		self.root = self._delMin(self.root)

	def _delMin(self, node):
		if node.left is None:
			return node.right
		node.left = self._delMin(node.left)
		return node

	def max_depth(self):
		return self._max_depth(self.root)

	def _max_depth(self, node):
		if node is None:
			return 0
		else:
			return 1 + max(self._max_depth(node.left), self._max_depth(node.right))

	def size(self):
		return self.__size__(self.root)

	def __size__(self, node):
		if node is None:
			return 0
		return self.__size__(node.left) + 1 + self.__size__(node.right)

	def __print__(self):
		"""
		print nodes in descending order
		"""
		def _print(node):
			if node is None:
				return
			if node.left:
				_print(node.left)
			print(node.data)
			if node.right:
				_print(node.right)

		_print(self.root)



def main():
	a = LLRBT()
	data = range(100, 1, -1)
	map(lambda x: a.put(x), data)
	a.__print__()
	#print a
	print('rank=%s' % a.rank(42))
	print('min=%s' % a.min().data)
	print('maxDepth=%s' % a.max_depth())
	from math import log
	print('size=%s logsize=%s' % (a.size(), log(a.size(), 2) +1))

if __name__ == "__main__":
	main()