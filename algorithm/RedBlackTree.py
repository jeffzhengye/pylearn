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
		self.root = self.__put__(self.root, data)

	def __put__(self, h, data):
		if h is None: return Node(data)
		if data < h.data:
			h.left = self.__put__(h.left, data)
		elif data > h.data:
			h.right = self.__put__(h.right, data)
		else:
			h.data = data
			return h

		if isRed(h.right) and not isRed(h.left):
			h = self.rotateLeft(h)
		if isRed(h.left) and isRed(h.left.left):
			h = self.rotateRight(h)
		if isRed(h.left) and isRed(h.right):
			h = self.__flipColors__(h)
		return h

	def __flipColors__(self, h):
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
		return self.__search__(self.root, data)

	def __search__(self, node, data):
		if node is None:
			return None
		if data == node.data:
			return node
		elif data < node.data:
			return self.__search__(node.left, data)
		else:
			return self.__insert__(node.right, data)

	def floor(self, data):
		return self.__floor__(self.root, data)

	def __floor__(self, node, data):
		if node is None:
			return None
		if data == node.data:
			return node
		if data < node.data:
			return self.__floor__(node.left, data)

		t = self.__floor__(node.righ, data)
		if t is not None:
			return t
		else:
			return node

	def ceiling(self, data):
		return self.__ceiling__(self.root, data)

	def __ceiling__(self, node, data):
		pass

	def rank(self, data):
		return self.__rank__(self.root, data)

	def __rank__(self, node, data):
		if node is None: return 0
		if data < node.data:
			return self.__rank__(node.left, data)
		elif data > node.data:
			return self.__size__(node.left) + 1 + self.__rank__(node.right, data)
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
		return self.__min__(self.root)

	def __min__(self, node):
		if node.left is None:
			return node
		else:
			return self.__min__(node.left)

	def delMin(self):
		self.root = self.__delMin__(self.root)

	def __delMin__(self, node):
		if node.left is None:
			return node.right
		node.left = self.__delMin__(node.left)
		return node

	def max_depth(self):
		return self.__max_depth__(self.root)

	def __max_depth__(self, node):
		if node is None:
			return 0
		else:
			return 1 + max(self.__max_depth__(node.left), self.__max_depth__(node.right))

	def size(self):
		return self.__size__(self.root)

	def __size__(self, node):
		if node is None:
			return 0
		return self.__size__(node.left) + 1 + self.__size__(node.right)

	def printOrderedTree(self):
		"""
		"""
		self.__print__(self.root)

	def __print__(self, node):
		if node is None:
			return
		if node.left:
			self.__print__(node.left)
		print(node.data)
		if node.right:
			self.__print__(node.right)


def main():
	a = LLRBT()
	data = range(100, 1, -1)
	map(lambda x: a.put(x), data)
	a.printOrderedTree()
	print('rank=%s' % a.rank(42))
	print('min=%s' % a.min().data)
	print('maxDepth=%s' % a.max_depth())
	from math import log
	print('size=%s logsize=%s' % (a.size(), log(a.size(), 2)))

if __name__ == "__main__":
	main()