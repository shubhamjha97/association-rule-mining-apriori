from timing_wrapper import timeit

class Node:
	
	def __init__(self, k, max_leaf_size, depth):
		#self.isLeaf=False
		self.max_leaf_size = max_leaf_size
		self.depth=depth
		self.children={}
		self.k=0
		self.isTree=False

	def add(self, candidate):
		self.children[tuple(candidate)] = 0


class Tree:
	def __init__(self, c_list, k=3, max_leaf_size=3, depth=0):
		self.depth=depth
		self.children={}
		self.k=k
		self.max_leaf_size=max_leaf_size
		self.isTree=True
		self.build_tree(c_list)
		

	def update_tree(self):
		for child in self.children:
			if len(self.children[child].children) > self.max_leaf_size:
				child=Tree(self.children[child].children.keys(), k=self.k, max_leaf_size=self.max_leaf_size, depth=self.depth+1)

	def build_tree(self, c_list):
		for candidate in c_list:
			if candidate[self.depth]%self.k not in self.children:
				self.children[candidate[self.depth]%self.k]=Node(k=self.k, max_leaf_size=self.max_leaf_size, depth=self.depth)
			self.children[candidate[self.depth]%self.k].add(candidate)
		self.update_tree()

	def check(self, candidate, update=False):
		support=0
		if candidate[self.depth]%self.k in self.children:
			child = self.children[candidate[self.depth]%self.k]
			if child.isTree:
				support = child.check(candidate)
			else:
				if tuple(candidate) in list(child.children.keys()):
					if update:
						child.children[tuple(candidate)]+=1
						# print('count updated to', child.children[tuple(candidate)])
					return child.children[tuple(candidate)]
				else:
					return 0
		return support

def generate_subsets(transaction, k):
	res=[]
	n = len(transaction)
	transaction.sort()

	def recurse(transaction, k, i=0, curr=[]):
		if k==1:
			for j in range(i,n):
				res.append(curr + [transaction[j]])
			return None
		for j in range(i,n-k+1):
			temp= curr+ [transaction[j]]
			recurse(transaction, k-1, j+1, temp[:])
	recurse(transaction, k)

	return res


if __name__=='__main__':
	# temp_list=[[1,2,3],[2,3,4],[3,5,6],[4,5,6],[5,7,9],[7,8,9],[4,7,9]]
	temp_list_1=[[1], [2], [3], [4], [5], [6], [7], [8], [9]]
	t=Tree(temp_list_1, k=3, max_leaf_size=3, depth=0)
	#print(len(t.children))
	
	t.check([1], update=True)
	# for x in t.children.keys():
	# 	print(t.children[x].children)
	print(t.check([1], update=False))
	# print(generate_subsets([1,2,3,5,6], 3))
	# print(generate_subsets([1,2,3,5,6,8,0,13,45],3))
	# for x in t.children.keys():
	# 	print(t.children[x].children)