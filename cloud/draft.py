import pandas as pd
from sklearn.cross_validation import StratifiedShuffleSplit
import numpy as np

def group_data(df, keys):
    for key in keys:
        if 'AGE' in key:
                df[key] = pd.qcut(df[key], 2, labels=[0,1])
    labels = [ '.'.join([str(df[key][i]) for key in keys]) for i in range(len(df))]
    cellsize = np.unique(labels, return_counts=True)[1]
    mask = np.where(cellsize < 2)

    return labels

def split_data(df, keys, num_iter=3, random_state=0):
    labels = group_data(df, keys)
    return StratifiedShuffleSplit(labels, num_iter, test_size=0.5, random_state=random_state)

filename = 'Phenotypic_V1_0b_preprocessed1.csv'

csv = pd.read_csv(filename)

keys = ['AGE_AT_SCAN', 'SITE_ID']

sss = split_data(csv, keys, num_iter=3, random_state=0)

assess = []

for index_a, index_b in sss:
    set_a, set_b = csv.iloc[index_a], csv.iloc[index_b]
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
    
