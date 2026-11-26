# Dataset from : https://www.kaggle.com/datasets/heeraldedhia/groceries-dataset#:~:text=To%20put%20it%20another%20way%2C%20it%20allows,orders%20of%20people%20from%20the%20grocery%20stores.
from os import _exit
from sys import stderr
from itertools import chain, combinations
from types import NoneType
import readline
import pandas as pd
import numpy as np

min_support = int(input("Give the minimum support: "))#min_support = np.float64(input('Give the minimal support'))
min_conf = float(input("Give confidence: "))

# Read the dataset to a dataframe
dataframe = pd.read_csv('Groceries_dataset.csv')

#groupby to turn the dataframe
dataset = (dataframe.groupby(['Member_number', 'Date', 'itemDescription'])
           .size().unstack(fill_value=0) > 0)

# To keep the item labels
dataset_item_labels = dataset.columns.to_list()

# Turn the dataset into an array
dataset_array = dataset.to_numpy()

# For testing if the results are the same
# def apriori_test():
#     from mlxtend.frequent_patterns import apriori, association_rules
#     freq = apriori(dataset, min_support=min_support/dataset.shape[0], use_colnames=True)
#     rules = association_rules(freq, metric='confidence', min_threshold=min_conf)
#     print(rules.sort_values('confidence', ascending=False)
#                [['antecedents', 'consequents', 'support', 'confidence', 'lift']].head())

def get_powerset(set):
    return chain.from_iterable(combinations(set, r) for r in range(len(set)+1))

def pretty_print(C: list, title: str | None = None, output: str | None = None):
    f = open(output, 'a') if output is not None else None
    if title:
        print(title, file = f)
    for name, c in C:
        print(name, c, file = f)

def print_opts():
    print('''
          ---Options---
          i: insert items, separated by a comma
          h: show this menu
          a: print all the valid items
          q: quit
          ''')

def give_recommendations():
    items = input("Input a list of items, separated by a comma ('exit' to exit): ").split(',')
    while(items[0] == ''):
        print("No items given")
        items = input("Input a list of items, separated by a comma ('exit' to exit): ").split(',')
    if items[0] == 'exit':
        return


    # Start from all the items, test if they have a rule, and then test for each subset of the items
    items_powerset = list(get_powerset(items))
    for subset in reversed(items_powerset[1:]):
        for rule in rules:
            if subset == rule[0]:
                print(f"RECOMMENDATION FROM {subset} -> {rule[1]}")

def handle_opt():
    opt = input(">>: ")
    match opt:
        case 'h':
            print_opts()
            return
        case 'i':
            give_recommendations()
            return
        case 'a':
            for item in dataset_item_labels:
                print(item)
            return
        case 'q':
            print('Quitting')
            return 1
        case _:
            print("Invalid option (input 'h' for help)")
            return

def handle_the_rest(rules = None):
    print_opts()
    while(True):
        if handle_opt():
            break
    _exit(1)

def to_index_list(L):
    return [dataset_item_labels.index(x) for x in L]

def create_initial_candidate():
    #C = list[tuple[list[str], int]]
    C = []
    a = dataset_array.shape[0]
    for item in range(len(dataset_item_labels)):
        c = 0
        for t in range(a):
            c += dataset_array[t][item]
        C.append(([dataset_item_labels[item]], int(c)))
    return C

def create_next_candidate(C, k):
    #C = list[tuple[list[str], int]]
    list = []
    C_length = len(C)

    # The distinction is make for k = 1 here so we dont compute the requirement
    # that each combination has to have the first k-1 elements common
    if k == 1:
        for i in range(C_length - 1):
            for j in range(i+1, C_length):
                # This appends both full lists, and not just the names
                list.append(([C[i][0][0], C[j][0][0]], 0))
    else:
        # TODO: replace the for loop with a while, since when and item doesnt find a match in the list, the rest of them arent going to be matches
        for i in range(C_length - 1):
            for j in range(i+1, C_length):
                flag = True
                for t in range(k - 1):
                    if C[i][0][t] != C[j][0][t]:
                        flag = False
                        break
                if flag == True:
                    # append to the list, with the first element of the list in the tuple being the identical items
                    # append to the tuple list the last element of the list we are comparing, since they are the same
                    temp = C[i][0] + [C[j][0][k-1]]
                    list.append((temp, 0))

    populate(list)
    return list

def prune(candidate, min_support):
    c = []
    for i in range(len(candidate)):
        if candidate[i][1] >= min_support:
            c.append((candidate[i][0], candidate[i][1]))
        else:
            print(f"Candidate {candidate[i][0]} rejected due to Apriori rule", file=stderr)
    return c

def get_count(index_list):
    return dataset_array[:, index_list].all(axis=1).sum()

def populate(C):
    shape = dataset_array.shape
    for i in range(len(C)):
        l = C[i][0]
        index_list = []
        for j in range(len(l)):
            index = dataset_item_labels.index(l[j])
            if index == -1:
                print(f"{l[j]} is not in the dataset. Breaking")
                return -1
            index_list.append(index)
        C[i] = (C[i][0], get_count(index_list))

def calculate_rules(frequent_itemsets, min_conf):
    rules = []
    for L_k in frequent_itemsets:
        for itemset_tuple in L_k:
            itemset_list = itemset_tuple[0]
            itemset_count = itemset_tuple[1]
            powerset = list(get_powerset(itemset_list))
            for subset in powerset[1:-1]: # Skipping the first element which is the empty set, and the last which is the set itself, not a subset
                B = [x for x in itemset_list if x not in subset]
                # print("itemset_list: ", itemset_list)
                # print("Subset: ", subset)
                # print("B = X - A: ", B)
                dataset_total_length = dataset_array.shape[0]
                support_subset_B =  itemset_count / dataset_total_length
                support_subset = get_count(to_index_list(subset)) / dataset_total_length
                confidence = support_subset_B / support_subset
                if confidence >= min_conf:
                    rule = (subset, B, confidence, support_subset_B)
                    rules.append(rule)

    rules.sort(key=lambda r:r[2], reverse=True)
    return rules


#transactions = dataset_array.shape[0]
candidate_file = "candidate_file.txt"
frequent_file = "frequent_file.txt"

#reset both files
with open(candidate_file, 'w') as f:
    f.write('')
with open(frequent_file, 'w') as f:
    f.write('')

C_k = create_initial_candidate()
k = 1
#pretty_print(C_k, title = f"Candidate list for k = {k}")
pretty_print(C_k, title = f"Candidate list for k = {k}", output = candidate_file)

frequent_itemsets = []
L_k = []
while(len(C_k) != 0):

    #Create the list by pruning
    pruned_candidate = prune(C_k, min_support)
    if len(pruned_candidate) == 0:
        break
    L_k = pruned_candidate
    frequent_itemsets.append(L_k)
    #pretty_print(L_k, title = f"Frequent list for k = {k}")
    pretty_print(L_k, title = f"Frequent list for k = {k}", output = frequent_file)

    #Create the next candidate
    next_candidate = create_next_candidate(L_k, k)

    #Check if the new candidate is an empty set and end
    if len(next_candidate) == 0:
        break
    C_k = next_candidate
    k += 1
    #pretty_print(C_k,  title = f"Candidate list for k = {k}")
    pretty_print(C_k,  title = f"Candidate list for k = {k}", output = candidate_file)

if len(frequent_itemsets) < 2:
    print("Couldnt calculate proper rules for the specified support and confidence.")
    pretty_print(frequent_itemsets)
    handle_the_rest()

rules = calculate_rules(frequent_itemsets, min_conf)
for antecendent, consequent, confidence, support in rules:
    print(f'{antecendent} -> {consequent}: confidence = {confidence:.4f} | support: {support:.4f}')

handle_the_rest(rules)
