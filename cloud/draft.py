import pandas as pd
from sklearn.cross_validation import StratifiedShuffleSplit
import numpy as np
import os

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

def assign_filename(df, base_directory, key_in='FILE_ID', key_out='FILENAME', postfix='_reho.nii.gz'):
    df[key_out] = [os.path.join(base_directory, '%s%s' % (file_id, postfix))
                for file_id in df[key_in]]


filename = 'Phenotypic_V1_0b_preprocessed1.csv'
basedir = ''
key_filename = 'FILENAME'
key_target = 'DX_GROUP'
num_iter = 3

# columns to use
columns = ['subject', 'SITE_ID', 'FILE_ID', 'DX_GROUP', 'SEX', 'AGE_AT_SCAN']

csv = pd.read_csv(filename)
df = pd.DataFrame()
for column in columns:
        df[column] = csv[column]

# column of filenames
assign_filename(df, basedir, key_in='FILE_ID', key_out=key_filename, postfix='_reho.nii.gz')

# exclude rows without files
#to_exclude = [i for i in range(len(df)) if not os.path.isfile(df[key_filename].iloc[i])]
to_exclude = [i for i in range(len(df)) if 'no_filename' in df[key_filename].iloc[i]] # temp
df_sub = df.drop(df.index[to_exclude], inplace=False)

keys = ['DX_GROUP', 'SEX', 'AGE_AT_SCAN', 'SITE_ID']

df_sub, sss = split_data(df_sub, keys, num_iter=num_iter, random_state=0)

#dataset = {}
# read data
#for i in range(len(df_sub)):
#    dataset['t1w'] = [ nib.load(filename).get_data() for filename in df_sub[key_filename] ]

assess = []

# iteration
results = []
for i, (index_a, index_b) in enumerate(sss):
    print
    print 'iteration %s/%s' % (i+1, num_iter)
    set_a, set_b = df_sub.iloc[index_a], df_sub.iloc[index_b]
    
    set_a.to_csv('split1.csv')
    set_b.to_csv('split2.csv')

    print '''
    df_result = pd.DataFrame()
    # Model 1
    model_1a = Method_1.train(set_a)
    model_1b = Method_1.train(set_b)
    
    predict_model_1a_set_b = Method_1.test(model_1a, set_b)
    predict_model_1b_set_a = Method_1.test(model_1b, set_a)
    df_result['predict_model_1a_set_b'] = predict_model_1a_set_b
    df_result['predict_model_1b_set_a'] = predict_model_1b_set_a
    df_result['rss_model_1a_set_b'] = ((df_result['predict_model_1a_set_b'] - df_sub[key_target])**2).sum()
    df_result['rss_model_1b_set_a'] = ((df_result['predict_model_1b_set_a'] - df_sub[key_target])**2).sum()
    
    # Model 2
    # ...
    
    results.append((set_a, set_b, df_result))
    '''
    # run training
    #train(index_a)
    #train(index_b)

    # test data
    #predict_a = test(index_a)
    #predict_b = test(index_b)

    # evaluate
    #something = some_kind_of_distance(predict_a, predict_b)
    #assess.append(something)


