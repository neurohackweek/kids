import pandas as pd
from sklearn.cross_validation import StratifiedShuffleSplit
import numpy as np

def group_data(df, keys):
    for key in keys:
        if 'AGE' in key:
            df[key] = pd.qcut(df[key], 2, labels=[0,1])
    labels = [ '.'.join([str(df[key].iloc[i]) for key in keys]) for i in range(len(df))]
    rows, index, count = np.unique(labels, return_index=True, return_counts=True)

    # sub_dataframe 
    df_sub = df.drop(df.index[index[count==1].tolist()], inplace=False)
    for row in rows[count==1]:
        labels.remove(row)

    return df_sub, labels

def split_data(df, keys, num_iter=3, random_state=0):
    df_sub, labels = group_data(df, keys)
    return df_sub, StratifiedShuffleSplit(labels, num_iter, test_size=0.5, random_state=random_state)

filename = 'Phenotypic_V1_0b_preprocessed1.csv'

csv = pd.read_csv(filename)

keys = ['AGE_AT_SCAN', 'SITE_ID']

csv_sub, sss = split_data(csv, keys, num_iter=3, random_state=0)

assess = []

for index_a, index_b in sss:
    set_a, set_b = csv_sub.iloc[index_a], csv_sub.iloc[index_b]
    set_a.to_csv('split1.csv')
    set_b.to_csv('split2.csv')

    # image data[index_a/b]
    
    # run training
    #train(index_a)
    #train(index_b)
    
    # test data
    #predict_a = test(index_a)
    #predict_b = test(index_b)
    
    # evaluate
    #something = some_kind_of_distance(predict_a, predict_b)
    #assess.append(something)
    
