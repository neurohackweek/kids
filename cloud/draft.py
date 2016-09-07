import pandas as pd
from sklearn.cross_validation import StratifiedShuffleSplit
import numpy as np

def split_data(df, keys, num_iter=3, random_state=0):
    labels = [ '.'.join([str(df[key][i]) for key in keys]) for i in range(len(df))]
    return StratifiedShuffleSplit(labels, num_iter, test_size=0.5, random_state=random_state)

filename = 'Phenotypic_V1_0b_preprocessed1.csv'

csv = pd.read_csv(filename)

keys = ['AGE_AT_SCAN', 'SEX']

# age -> 0:young/1:old (median)
for key in keys:
    if 'AGE' in key:    # TODO: better way?
    #if len(df[key].unique())>2:
        key_binary = '%s_binary' % key
        csv[key_binary] = pd.qcut(df[key], 2, labels=[0,1])
        keys[i] = key_binary

sss = split_data(csv, keys, num_iter=3, random_state=0)
print sss
assess = []
for index_a, index_b in sss:
    #print("TRAIN:", index_a, "TEST:", index_b)
    set_a, set_b = csv.iloc[index_a], csv.iloc[index_b]
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
    
