"""
Python Recursive implementation of BST
"""
__author__ = 'zheng'


class Node:
	def __init__(self, data=None):
		self.data = data
		self.left = None
		self.right = None
		self.count = 0


class BST:
	def __init__(self):
		self.root = None

	def insert(self, data):
		if not self.root:
			self.root = Node(data)
		else:
			self.__insert__(self.root, Node(data))

	def __insert__(self, node, dNode):
		if dNode.data < node.data:
			if node.left is None:
				node.left = dNode
			else:
				self.__insert__(node.left, dNode)
		else:  ##if equals right, insert as right child
			if node.right is None:
				node.right = dNode
			else:
				self.__insert__(node.right, dNode)

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


	def maxdepth(self):
		pass

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
	a = BST()
	a.insert(4)
	a.insert(34)
	a.insert(45)
	a.insert(46)
	a.insert(41)
	a.insert(48)
	a.insert(46)
	a.printOrderedTree()
	print('size=%s' % a.size())
	print('rank=%s' % a.rank(42))
	print('min=%s' % a.min().data)

if __name__ == "__main__":
	main()