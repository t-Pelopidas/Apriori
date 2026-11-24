# Dataset from : https://www.kaggle.com/datasets/heeraldedhia/groceries-dataset#:~:text=To%20put%20it%20another%20way%2C%20it%20allows,orders%20of%20people%20from%20the%20grocery%20stores.
from types import NoneType

import pandas as pd
import numpy as np
import aprioriHelpers as ah
import helpers as h

min_support = int(input("Give the minimum support: "))#min_support = np.float64(input('Give the minimal support'))
min_conf = input("Give confidence: ")

# Read the dataset to a dataframe
dataframe = pd.read_csv('Groceries_dataset.csv')


#groupby to turn the dataframe
dataset = (dataframe.groupby(['Member_number', 'Date', 'itemDescription'])
           .size().unstack(fill_value=0) > 0).astype(int)

# To keep the item labels
dataset_item_labels = dataset.columns.to_list()

# Turn the dataset into an array
dataset_array = dataset.to_numpy()

#transactions = dataset_array.shape[0]
candidate_file = "candidate_file.txt"
list_file = "list_file.txt"

#reset both files
with open(candidate_file, 'w') as f:
    f.write('')
with open(list_file, 'w') as f:
    f.write('')

C_k = ah.create_initial_candidate(dataset_item_labels, dataset_array)
k = 1
h.pretty_print(C_k, title = "Next candidate", f = candidate_file)

# k = 1
# C_k
# while C_k != 0
    # L_k = Prune(C_k)
    # create C_(k+1)
frequent_itemsets = []
L_k = []
while(len(C_k) != 0):

    #Create the list by pruning
    pruned_candidate = ah.prune(C_k, min_support)
    if len(pruned_candidate) == 0:
        break
    L_k = pruned_candidate
    frequent_itemsets.append(L_k)
    h.pretty_print(L_k, title = "Next List", f = list_file)

    #Create the next candidate
    next_candidate = ah.create_next_candidate(L_k, k, dataset_item_labels, dataset_array)

    #Check if the new candidate is an empty set and end
    if len(next_candidate) == 0:
        break
    C_k = next_candidate
    h.pretty_print(C_k,  title = "Next candidate", f = candidate_file)
    k += 1

rules = ah.calculate_rules(L_k, min_conf)
print("Computation finished")
h.print_opts()
while(True):
    transaction_list = h.handle_opt(dataset_item_labels)
    if transaction_list == -1:
        break
    elif type(transaction_list) == NoneType:
        continue
