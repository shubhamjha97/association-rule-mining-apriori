import csv
import itertools
from time import time
import numba as nb

MINSUP=3
HASH_DENOMINATOR=10
K_MAX=10

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

@timeit
def subset(c_list, transactions):
	candidate_counts={}
	for transaction in transactions:
		for candidate in c_list:
			if set(candidate).issubset(set(transaction)):
				candidate_counts[tuple(candidate)]=candidate_counts.get(tuple(candidate), 0)
				#print(candidate_counts[tuple(candidate)])
				candidate_counts[tuple(candidate)]+=1
	print(candidate_counts)
	return candidate_counts

def frequent_itemset_generation(data_path):
	transactions, items=load_data(data_path)
	print('Found', len(transactions), 'transactions,', len(items), 'items.')
	map_=create_map(items)
	one_itemset=[[itemset] for itemset in items][0:100]
	items_mapped=[applymap(itemset, map_) for itemset in one_itemset]
	transactions_mapped = [applymap(transaction, map_) for transaction in transactions]
	l_current=items_mapped

	L_final=[]

	for i in range(K_MAX):	###############
		c_current=apriori_gen(l_current) ##############
		if len(c_current):
			C_t=subset(c_current, transactions_mapped)
			l_current=[]
			for c in C_t.keys():
				if C_t[c]>MINSUP:
					l_current.append(c)
			L_final.append(l_current)
		else:
			break

	return L_final

if __name__=='__main__':
	data_path='data/groceries.csv'
	frequent_itemset_generation(data_path)