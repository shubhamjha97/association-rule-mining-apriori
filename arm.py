import csv
import itertools
from time import time
import numba as nb

MINSUP=100

def timeit(fn):
	def wrapper(*args, **kwargs):
		start=time()
		res=fn(*args, **kwargs)
		print(fn.__name__, "took", time()-start, "seconds.")
		return res
	return wrapper

@timeit
def load_data(path):
	items=[]
	with open(path, 'r') as f:
	    reader = csv.reader(f)
	    transactions = list(reader)
	for x in transactions:
		items.extend(x)
	items=sorted(set(items))
	return transactions, items

def create_map(items):
	return {x:i for i,x in enumerate(items)}

def applymap(transaction, map_):
	ret=[]
	for item in transaction:
		ret.append(map_[item])
	return ret

@timeit
def apriori_gen(l_prev):
	n=len(l_prev)
	l_curr=[]
	for i in range(n):
		for j in range(i+1, n):
			temp_a = l_prev[i]
			temp_b = l_prev[j]
			if temp_a[:-1]==temp_b[:-1]:
				temp_c=[]
				temp_c.extend(temp_a)
				temp_c.append(temp_b[-1])
				l_curr.append(temp_c)
	return l_curr

def subset(c_list, transactions):
	return {}

def frequent_itemset_generation(data_path):
	transactions, items=load_data(data_path)
	print('Found', len(transactions), 'transactions,', len(items), 'items.')
	map_=create_map(items)
	one_itemset=[[itemset] for itemset in items][0:100]
	items_mapped=[applymap(itemset, map_) for itemset in one_itemset]
	#c_dict={}
	#k=1
	l_current=items_mapped
	for i in range(10):	###############
		c_current=apriori_gen(l_current) ##############
		for t in transactions:
			C_t=subset(c_current, transactions)
		l_current=[]
		for c in C_t.keys():
			if C_t[c]:
				l_current.append(c)
if __name__=='__main__':
	data_path='data/groceries.csv'
	frequent_itemset_generation(data_path)