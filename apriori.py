# Dataset from : https://www.kaggle.com/datasets/heeraldedhia/groceries-dataset#:~:text=To%20put%20it%20another%20way%2C%20it%20allows,orders%20of%20people%20from%20the%20grocery%20stores.

import pandas as pd
import numpy as np
from pandas.io.stata import find_stack_level
import helpers as h

min_support = np.float64(25)#min_support = np.float64(input('Give the minimal support'))
#confidence = input('Give confidence')
# Read the dataset to a dataframe
dataframe = pd.read_csv('Groceries_dataset.csv')

#groupby to turn the dataframe
dataset = (dataframe.groupby(['Member_number', 'Date', 'itemDescription'])['itemDescription'].count().unstack().fillna(0))
# To keep the item labels
dataset_item_labels = dataset.columns.to_list()

# Turn the dataset into an array
dataset_array = dataset.to_numpy()

#transactions = dataset_array.shape[0]

with open("iterations.txt", 'w') as f:
    f.write('')
C_k = h.create_initial_candidate(dataset_item_labels, dataset_array)
k = 1
h.pretty_print(C_k)

print(np.unique(dataset_array))          # all distinct values; a binary array gives [0., 1.]
print(dataset_array.max())               # > 1 means not binary
print((dataset_array > 1).sum())         # how many cells exceed 1 (should be 732)

print(dataset_array)
while(len(C_k) != 0):

    #Create the list by pruning
    print("Pruning")
    L_k = h.prune(C_k, min_support)
    #Create the next candidate
    next_candidate = h.create_next_candidate(L_k, k)
    print("Next candidate generated:")
    print("Populating")
    if h.populate(next_candidate, dataset_item_labels, dataset_array) == -1:
        print("populate failed: exiting")
    if len(next_candidate) == 0:
        break
    C_k = next_candidate
    h.pretty_print(C_k)
    k += 1
print("end")
