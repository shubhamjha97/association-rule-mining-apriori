# Association rules mining
Association rules mining using Apriori algorithm.

Course Assignment for CS F415- Data Mining @ BITS Pilani, Hyderabad Campus.

**Done under the guidance of Dr. Aruna Malapati, Assistant Professor, BITS Pilani, Hyderabad Campus.**

## Table of Contents
* [Instructions to run the scripts](#instructions-to-run-the-scripts)
  * [Create the train matrix and the mappings](#create-the-train-matrix-and-the-mappings)
  * [Collaborative Filtering](#collaborative-filtering)
  * [Collaborative Filtering with Baseline Approach](#collaborative-filtering-with-baseline-approach)
  * [SVD](#svd)
  * [CUR](#cur)
* [Introduction](#introduction)
* [Data](#data)
* [Directory Structure](#directory-structure-)
* [Basic Collaborative Filtering](#basic-collaborative-filtering)
* [Collaborative Filtering with baseline](#collaborative-filtering-with-baseline)
* [SVD](#svd-1)
* [CUR](#cur-1)
* [Machine specs](#machine-specs-)
* [Results](#results)
* [Members](#members)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Instructions to run the scripts
Run the following commands:

##### Create the train matrix and the mappings
```python
python arn.py
```

## Important variables
```python
MINSUP - Minimum support
HASH_DENOMINATOR - Denominator for the hash function (For support counting using hash tree)
MIN_CONF - Minimum confidence
```

## Introduction
Association rules mining is a rule-based method for discovering interesting relations between variables in large databases. It is intended to identify strong rules discovered in databases using some measures of interestingness. We used confidence as a measure of interestingness.
The main purpose of this project is to get an in depth understanding of how the Apriori algorithm works.
We implemented support counting using hash trees. The difference between out approach is significant as demonstrated by the following run times (we used the same value of ```MINSUP``` and ```MIN_CONF``` for both)-

Support counting using hash tree- ```22.5 s```
Support counting using brute force- ```5.9 s ```

* More on [Association rule learning](https://en.wikipedia.org/wiki/Association_rule_learning). *

## Data
We used the Groceries Market Basket Dataset, which can be found [here](http://www.sci.csueastbay.edu/~esuess/classes/Statistics_6620/Presentations/ml13/groceries.csv). The dataset contains *9835* transactions by customers shopping for groceries. The data contains *169* unique items. The data can be found in the folder *data*.

## Directory Structure:

```
association-rule-mining-apriori/
+-- data
|   +-- groceries.csv (original data file containing transactions)
+--  arm.py(python script to read the data, mine frequent itemsets and interesting rules)
+--  hash_tree.py(python file containing the Tree and Node classes used to build the hash tree for support counting)
+--  timing_wrapper.py(python decorator used to measure execution time of functions)
+--  l_final.pkl(all the frequent itemsets in pickled format)
+--  frequent_itemsets.txt(all the frequent itemsets presented in the prescribed format)
+--  association_rules.txt(all the interesting association rules mined and presented in the prescribed format)
+--  reverse_map.pkl(mapping from items to index in pickled format)
```

## Prescribed format of output
##### Association Rules
Precedent (itemset (support count)) ---> Antecedent (itemset (support count)) - confidence value
##### Frequent itemsets
Frequent itemset (support count)

## Machine specs:
Processor: i7-7500U

Ram: 16 GB DDR4

OS: Ubuntu 16.04 LTS

## Results

| Recommender System Technique               | Root Mean Square Error (RMSE)   | Precision on top K                  | Spearman Rank Correlation            | Time taken for prediction (secs) |
|--------------------------------------------|---------------------------------|-------------------------------------|--------------------------------------|----------------------------------|
| Collaborative                              | 2.033519 (item) 2.1502(user)    | 0.6016 (item) 0.584474(user)        | 0.99999975(item) 0.99999972 (user)   | 211.979 (item)  272.817 (user)   |
| Collaborative along with Baseline approach | 0.939036 (item) 1.005434 (user) | 0.62865586 (item) 0.64406025 (user) | 0.999999947 (item) 0.99999939 (user) | 313.3369 (item) 273.2009(user)   |
| SVD                                        | 1.03512426007                   | 0.654428981666                      | 0.999999999839                       | 565.33                           |
| SVD with 90% retained energy               | 1.03                            | 0.6528                              | 0.999999999839                       | 361.49                           |
| CUR                                        | 1.19389972                      | 0.900607466                         | 0.99999999786                        | 53.4029                          |

## Members
[Shubham Jha](http://github.com/shubhamjha97)

[Praneet Mehta](http://github.com/praneetmehta)

[Abhinav Jain](http://github.com/abhinav1112)