#!/usr/bin/env python

import pandas as pd
from sklearn.cross_validation import StratifiedShuffleSplit
import numpy as np
import os

def group_data(df, keys):
    '''
group_data(df, keys)
    To create a DataFrame with columns in keys that each combination of keys has more than 1 subject, and to convert age to binary value.
input:
    df: Pandas DataFrame
    keys: Column names (list)
output:
    df_sub: Pandas DataFrame with columns in keys. Each combination of keys has more than 1 subject.
    labels: list of dot-joined keys

'''
    for i, key in enumerate(keys):
        if 'AGE' in key:
            key_binary = '%s_binary' % key
            df[key_binary] = pd.qcut(df[key], 2, labels=[0,1])
            keys[i] = key_binary
    labels = [ '.'.join([str(df[key].iloc[i]) for key in keys]) for i in range(len(df))]
    rows, index, count = np.unique(labels, return_index=True, return_counts=True)

    # sub_dataframe 
    df_sub = df.drop(df.index[index[count==1].tolist()], inplace=False)
    for row in rows[count==1]:
        labels.remove(row)

    return df_sub, labels

def split_data(df, keys, num_iter=3, random_state=0):
    '''
split_data(df, keys, num_iter=3, random_state=0)
    To split a DataFrame into two matched samples.
input:
    df: Pandas DataFrame
    keys: Column names to be matched
    num_iter=3: number of iteration
    random_state=0: random seed
output:
    df_sub: DataFrame after excluding subjects of key combinations having 1 subject.
    sss: StratifiedShuffleSplit object containing num_iter sets of two group indices.
e.g.:
    df_sub, sss = split_data(df, ['DX_GROUP', 'SEX', 'AGE_AT_SCAN', 'SITE_ID'])
'''
    df_sub, labels = group_data(df, keys)
    return df_sub, StratifiedShuffleSplit(labels, num_iter, test_size=0.5, random_state=random_state)


if __name__ == '__main__':
    pass

