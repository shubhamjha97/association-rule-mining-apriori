import csv
import itertools
from time import time
#import numba as nb
import pickle
import os

MINSUP=50
HASH_DENOMINATOR=10
K_MAX=10
MIN_CONF=0.0000001

def timeit(fn):
	def wrapper(*args, **kwargs):
		start = time()
		res = fn(*args, **kwargs)
		print(fn.__name__, "took", time() - start, "seconds.")
		return res
	return wrapper

@timeit
def load_data(path):
	items = []
	with open(path, 'r') as f:
	    reader = csv.reader(f)
	    transactions = list(reader)
	for x in transactions:
		items.extend(x)
	items=sorted(set(items))
	return transactions, items

def create_map(items):
	map_ = {x:i for i,x in enumerate(items)}
	reverse_map = {i:x for i,x in enumerate(items)}
	return map_, reverse_map

def applymap(transaction, map_):
	ret = []
	for item in transaction:
		ret.append(map_[item])
	return ret

@timeit
def apriori_gen(l_prev):
	n = len(l_prev)
	c_curr = []
	for i in range(n):
		for j in range(i+1, n):
			temp_a = l_prev[i]
			temp_b = l_prev[j]
			if temp_a[:-1] == temp_b[:-1]:
				temp_c = []
				temp_c.extend(temp_a)
				temp_c.append(temp_b[-1])
				temp_c=sorted(temp_c)
				c_curr.append(temp_c)
	return c_curr

@timeit
def subset(c_list, transactions):
	candidate_counts={}
	for transaction in transactions:
		for candidate in c_list:
			if set(candidate).issubset(set(transaction)):
				candidate_counts[tuple(candidate)] = candidate_counts.get(tuple(candidate), 0)
				candidate_counts[tuple(candidate)] += 1
	return candidate_counts

def frequent_itemset_generation(data_path):
	if 'l_final.pkl' in os.listdir('.'):
		return pickle.load(open('l_final.pkl', 'rb'))
	transactions, items = load_data(data_path)
	print('Found', len(transactions), 'transactions,', len(items), 'items.')
	map_, reverse_map = create_map(items)
	one_itemset = [[itemset] for itemset in items]
	items_mapped = [applymap(itemset, map_) for itemset in one_itemset]
	transactions_mapped = [applymap(transaction, map_) for transaction in transactions]
	temp_l_current = subset(items_mapped, transactions_mapped)

	#l_current={}

	#for t in temp_l_current.keys():
	#	if temp_l_current[t] > MINSUP:
	#		l_current[tuple(t)] = temp_l_current[t]

	L_final = []
	L_final.append(temp_l_current)
	l_current=temp_l_current

	for i in range(K_MAX):
		c_current = apriori_gen(list(l_current.keys()))
		if len(c_current):
			C_t = subset(c_current, transactions_mapped)
			l_current = {}
			for c in C_t.keys():
				if C_t[c] > MINSUP:
					l_current[tuple(sorted(c))] = C_t[c]
			if len(l_current):
				L_final.append(l_current)
		else:
			break
	pickle.dump(L_final, open('l_final.pkl', 'wb+'))
	return L_final

def generate_rules(frequent_items):
	rules=[]
	for k_itemset in frequent_items:
		k=len(list(k_itemset.keys())[0])
		if k==1:
			continue
		for itemset, support in k_itemset.items():
			H_curr=[[x] for x in itemset]
			for m in range(1,k-1):
				if k > m+1:
					H_next=apriori_gen(H_curr)
					print('h_next', H_next)
					to_remove=[]
					for h in H_next:
						X=tuple(sorted(set(itemset)-set(h)))
						Y=tuple(sorted(h))
						#print('k', k, 'm', m)
						#print('X:', X, 'Y:', Y)
						confidence=support/frequent_items[k-m-2][X]
						#print('X:', X, 'Y:', Y, 'conf', confidence)
						if confidence>MIN_CONF:
							rule=[]
							rule.append(X)
							rule.append(Y)
							rules.append(rule)
						else:
							to_remove.append(h)
					H_next=[x for x in H_next if x not in to_remove]
					#print('updated h_next', H_next)
					H_curr=H_next
				else:
					break	
	return rules


def display_rules(rules, write=False):
	with open('output.txt', 'w+') as f:
		for rule in rules:
			X=rule[0]
			Y=rule[1]
			print(X, '--->', Y)
			f.write(str(X)+'--->'+str(Y)+'\n')

if __name__=='__main__':
	data_path = 'data/groceries.csv'
	frequent_items = frequent_itemset_generation(data_path)
	rules = generate_rules(frequent_items)
	#print(rules)
	display_rules(rules, write=True)