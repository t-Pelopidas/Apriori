# Dataset from : https://www.kaggle.com/datasets/heeraldedhia/groceries-dataset#:~:text=To%20put%20it%20another%20way%2C%20it%20allows,orders%20of%20people%20from%20the%20grocery%20stores.
import pandas as pd
import numpy as np

def pretty_print(list):
    for i in range(len(list)):
          print(list[i])

def create_next_combination(current_combination, k, dsarray, dsil):
    l = len(current_combination)
    next_combination = []
    for i in range(l):
        for j in range(i+1, l):
            next_combination.append((current_combination[i][0], current_combination[j][0]))

    return next_combination

min_support = np.float64(100)#min_support = np.float64(input('Give the minimal support'))
#confidence = input('Give confidence')
# Read the dataset to a dataframe
dataframe = pd.read_csv('Groceries_dataset.csv')

#groupby to turn the dataframe
dataset = (dataframe.groupby(['Member_number', 'Date', 'itemDescription'])['itemDescription'].count().unstack().fillna(0))

# To keep the item labels
dataset_item_labels = dataset.columns.to_list()
# Turn the dataset into an array
dataset_array = dataset.to_numpy()
print(dataset_item_labels)
print(dataset_array)

transactions = dataset_array.shape[0]
items = len(dataset_item_labels)

# Filter by the min_support
def prune(combination):
    transaction = 0
    while(transaction < len(transactions_list)):
        print(f"Comparing: {transactions_list[transaction][1]} < {min_support}")
        if transactions_list[transaction][1] < min_support:
            print(f'Removing {transactions_list[transaction]} from the list')
            # When removing the order gets fucked and some items get skipped over
            transactions_list.remove((transactions_list[transaction]))
        else:
            transaction += 1

def create_list(combination):
    tuple = []
    for item in range(items):
        c = 0
        for tid in range(transactions):
            c += dataset_array[tid, item]
        tuple.append((dataset_item_labels[item], c))

    prune(tuple)
    return tuple

# For each item count the times it was purchased
transactions_list = dataset_item_labels
k = 0
while(True):

    # Create all the combinations on a new list
    next_combination =  create_next_combination(transactions_list, k, dataset_array, dataset_item_labels)
    pretty_print(next_combination)
    if len(next_combination) == 0:
        break
    combination = next_combination
    pretty_print(combination)

    transactions_list = create_list(next_combination)
    pretty_print(transactions_list)



    break

print("end")
