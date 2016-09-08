#!/usr/bin/env python

import pandas as pd
from sklearn.cross_validation import StratifiedShuffleSplit
import numpy as np
import os
import argparse
import sys

def group_data(df, keys, inplace=False):
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
            if inplace:
                df[key] = pd.qcut(df[key], 2, labels=[0,1])
            else:
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
    parser = argparse.ArgumentParser(description='csv file clean-up')
    parser.add_argument('pheno_file', help='File containing the participant'
    'information for the analysis that will be run. This is a CSV with the'
    'participant id in the first column and the dependent variable and '
    'regressors of no interest in the remaining columns.')
    parser.add_argument('outcome_csv', help='The outcome csv file', default='pheno.csv')
    parser.add_argument('-k', '--keys', help='comma(,)-separated key names to match',
            default="DX_GROUP,SEX,AGE_AT_SCAN,SITE_ID", dest='keys_match_str')
    parser.add_argument('-t', '--threshold', help='threshold value from fMRI motion',
            default=20, dest='motion_thresh')
    
    args = parser.parse_args()
    fn_csv = args.pheno_file
    fn_out = args.outcome_csv
    keys = [str(elmt) for elmt in args.keys_match_str.strip().split(',')]
    columns = ['subject', 'func_perc_fd', 'FILE_ID'] + keys
    out_columns = ['subject'] + keys

    print fn_csv, fn_out, keys
    print args

    if not os.path.isfile(fn_csv):
        sys.stderr.write('%s not exist\n' % fn_csv)
        sys.exit(-1)
    
    df = pd.read_csv(fn_csv)[columns]

    to_exclude = [i for i in range(len(df)) if 'no_filename' in df['FILE_ID'].iloc[i]]
    df_sub = df.drop(df.index[to_exclude], inplace=False)

    df_sub.drop(df_sub.index[df_sub['func_perc_fd'] < args.motion_thresh], inplace=True)

    df_sub, labels = group_data(df, keys, inplace=True)
    df_out = df_sub[out_columns]
    df_out.to_csv(fn_out, index=False)

