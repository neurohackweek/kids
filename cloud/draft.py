import pandas as pd
from sklearn.cross_validation import StratifiedShuffleSplit
import numpy as np

def split_data(df, keys, num_iter=3, random_state=0):
    output = df[keys].apply(lambda x: len(x.unique()))
    for key in keys:
	if len(df[key].unique())>2:
		df[key] = pd.qcut(df[key], 2, labels=[0,1])
    labels = [ '.'.join([str(df[key][i]) for key in keys]) for i in range(len(df))]
    return StratifiedShuffleSplit(labels, num_iter, test_size=0.5, random_state=0)

csv = pd.read_csv(filename)
sss = split_data(csv, keys, num_iter=3, random_state=0)
print sss
assess = []
for index_a, index_b in sss:
    #print("TRAIN:", train_index, "TEST:", test_index)
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
    
