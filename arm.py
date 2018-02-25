import csv
import itertools
from time import time
import pickle
import os
from hash_tree import Tree, generate_subsets
from timing_wrapper import timeit

# Important variables
MINSUP = 60 # Minimum support
HASH_DENOMINATOR = 10 # Denominator of the hash function
MIN_CONF = 0.5 # Minimum confidence

@timeit
def load_data(path):
	'''
	Function to read itemsets from file.

	Parameters
	----------
	path : string
	    path to file containinng transactions.
	
	Returns
	----------
	transactions : list
		list containing all transactions. Each transaction is a list of
		items present in that transaction.
	items : list
		list containing all the unique items.
	'''
	items = []
	with open(path, 'r') as f:
	    reader = csv.reader(f)
	    transactions = list(reader)
	for x in transactions:
		items.extend(x)
	items=sorted(set(items))
	return transactions, items

def create_map(items):
	'''
	Function to map unique items to integers.

	Parameters
	----------
	items : list
	    list of unique items.
	
	Returns
	----------
	map_ : dict
		Items --> integers mapping.
	reverse_map : dict	
		Integers --> items mapping.
	'''
	map_ = {x:i for i,x in enumerate(items)}
	reverse_map = {i:x for i,x in enumerate(items)}
	return map_, reverse_map

def applymap(transaction, map_):
	'''
	Function to apply mapping to items.

	Parameters
	----------
	transaction : list
	    single transaction.
	map_ : dict
	    mapping.
	
	Returns
	----------
	ret : dict
		mapped transaction.
	'''
	ret = []
	for item in transaction:
		ret.append(map_[item])
	return ret

#@timeit
def apriori_gen(l_prev):
	'''
	Function to generate c(k+1) from l(k).
	
	This function has been implemented as presented in Introduction to Data 
	Mining,Tan Pang-Ning et al, section 6.2.3
	Parameters
	----------
	l_prev : list
	    l(k)

	Returns
	----------
	c_curr : list
		c(k+1).
	'''
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

# Brute force subset generation and support counting
# @timeit
# def subset(c_list, transactions):
# 	candidate_counts={}
# 	for transaction in transactions:
# 		for candidate in c_list:
# 			if set(candidate).issubset(set(transaction)):
# 				candidate_counts[tuple(candidate)] = candidate_counts.get(tuple(candidate), 0)
# 				candidate_counts[tuple(candidate)] += 1
# 	return candidate_counts

@timeit
def subset(c_list, transactions):
	'''
	Function to get support counts of candidates.

	Parameters
	----------
	transaction : list
	    single transaction.
	map_ : dict
	    mapping.
	'''
	candidate_counts={}
	t=Tree(c_list, k=HASH_DENOMINATOR, max_leaf_size=100)
	for transaction in transactions:
		subsets =generate_subsets(transaction, len(c_list[0]))
		for sub in subsets:
			t.check(sub, update=True)
	for candidate in c_list:
		candidate_counts[tuple(candidate)] = t.check(candidate, update=False)
	return candidate_counts

def frequent_itemset_generation(data_path):
	'''
	Function to read data and generate frequent itemsets using the Apriori algorithm.

	Parameters
	----------
	data_path : string
	    path to file containing transactions.

	Returns
	----------
	L_final : list
		list of dictionaries containing the final L set.
	'''

	# Uncomment the following lines to load saved pickle file and avoid the extra time required
	# for frequent itemset generation.
	# if 'l_final.pkl' in os.listdir('.'):
	# 	return pickle.load(open('l_final.pkl', 'rb'))
	transactions, items = load_data(data_path)
	map_, reverse_map = create_map(items)
	pickle.dump(reverse_map, open('reverse_map.pkl', 'wb+'))
	one_itemset = [[itemset] for itemset in items]
	items_mapped = [applymap(itemset, map_) for itemset in one_itemset]
	transactions_mapped = [applymap(transaction, map_) for transaction in transactions]
	
	temp_l_current = subset(items_mapped, transactions_mapped)
	l_current={}
	for t in temp_l_current.keys():
		if temp_l_current[t] > MINSUP:
			l_current[tuple(t)] = temp_l_current[t]
	L_final = []
	L_final.append(l_current)

	while(len(l_current)):
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
	'''
	Function to generate rules from frequent itemsets.

	Parameters
	----------
	frequent_items : list
	    list containing all frequent itemsets.

	Returns
	----------
	rules : list
		list of generated rules.
	rules is stored in the following format-
	[(X, Y), (X,Y)]
	'''
	rules=[]
	for k_itemset in frequent_items:
		k=len(list(k_itemset.keys())[0])
		if k==1: # No rules can be generated using 1 itemsets
			continue
		for itemset, support in k_itemset.items():
			H_curr=[[x] for x in itemset]
			to_remove=[]
			for h in H_curr:
				X=tuple(sorted(set(itemset)-set(h)))
				Y=tuple(sorted(h))
				confidence = support / (frequent_items[k-2][X])
				if confidence > MIN_CONF:
					rule=[]
					rule.append(X)
					rule.append(Y)
					rules.append({tuple(rule):confidence})
				else:
					to_remove.append(h)

			H_curr=[x for x in H_curr if x not in to_remove]

			for m in range(1,k-1):
				if k > m+1:
					H_next=apriori_gen(H_curr)
					to_remove=[]
					for h in H_next:
						X=tuple(sorted(set(itemset)-set(h)))
						Y=tuple(sorted(h))
						confidence = support / (frequent_items[k-m-2][X])
						if confidence>MIN_CONF:
							rule=[]
							rule.append(X)
							rule.append(Y)
							rules.append({tuple(rule):confidence})
						else:
							to_remove.append(h)
					H_next=[x for x in H_next if x not in to_remove]
					H_curr=H_next
				else:
					break	
	return rules

def display_rules(rules, frequent_items, write=False):
	'''
	Function to display and write rules to file in the prescribed format.

	Prescribed Format
	-----------------
	Association Rules-
	Precedent (itemset (support count)) ---> Antecedent (itemset (support count)) - confidence value
	
	Frequent itemsets-
	Frequent itemset (support count)

	Parameters
	----------
	rules : list
	    list containing all rules generated by generate_rules function.
	frequent_items : list
	    list containing all frequent itemsets.
	write : bool
	    write to file if true. Two files are created- association_rules.txt and frequent_itemsets.txt
	'''
	reverse_map=pickle.load(open('reverse_map.pkl', 'rb'))
	bad_chars="[]''"
	with open('outputs/association_rules.txt', 'w+') as f:
		for rule in rules:
			X, Y=list(rule.keys())[0]
			precedent_support_count, antecedent_support_count=(frequent_items[len(X)-1][X], frequent_items[len(Y)-1][Y])
			confidence=list(rule.values())[0]
			print(str([reverse_map[x] for x in X]).strip(bad_chars).replace("'", '')+'('+str(precedent_support_count)+')'+' ---> '+str([reverse_map[y] for y in Y]).strip(bad_chars).replace("'", '') +'('+str(antecedent_support_count)+')' + ' - conf('+ str(confidence)+ ')')
			f.write(str([reverse_map[x] for x in X]).strip(bad_chars).replace("'", '')+'('+str(precedent_support_count)+')'+' ---> '+str([reverse_map[y] for y in Y]).strip(bad_chars).replace("'", '') +'('+str(antecedent_support_count)+')' + ' - conf('+ str(confidence)+ ')'+'\n')

	with open('outputs/frequent_itemsets.txt', 'w+') as f:
		for k_itemset in frequent_items:
			for itemset, support in k_itemset.items():
				f.write(str([reverse_map[x] for x in itemset]).strip(bad_chars).replace("'", '')+' ('+str(support)+')'+'\n')
			
if __name__=='__main__':
	data_path = 'data/groceries.csv'
	frequent_items = frequent_itemset_generation(data_path)
	rules = generate_rules(frequent_items)
	display_rules(rules, frequent_items, write=True)
	no_itemsets=0
	for x in frequent_items:
		no_itemsets+=len(x)
	print('No of rules:',len(rules), 'No of itemsets:', no_itemsets)