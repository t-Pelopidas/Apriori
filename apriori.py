# Dataset from : https://www.kaggle.com/datasets/heeraldedhia/groceries-dataset#:~:text=To%20put%20it%20another%20way%2C%20it%20allows,orders%20of%20people%20from%20the%20grocery%20stores.

import pandas as pd

#Read the dataset to a dataframe
df = pd.read_csv('Groceries_dataset.csv')

basket = df.groupby(['Member_number', 'Date'])

print(basket)

