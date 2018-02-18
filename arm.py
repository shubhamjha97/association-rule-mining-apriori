import csv

with open('groceries.csv', 'r') as f:
    reader = csv.reader(f)
    transactions = list(reader)

for i in transactions[:10]:
	print(i)

print(len(transactions))