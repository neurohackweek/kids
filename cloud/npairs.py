import pandas as pd
from sklearn.cross_validation import StratifiedShuffleSplit
import numpy as np
import os

assess = []
results = []	

df = pd.read_csv('dummy.csv')
colnames = df.keys()
labels = [ '.'.join([str(df[key].iloc[i]) for key in colnames[1:]]) for i in range(len(df))]
sss = StratifiedShuffleSplit(labels, 3, 0.5)

for i, (index_a, index_b) in enumerate(sss):
    print
    print 'iteration %s' % (i+1)
    set_a, set_b = df.iloc[index_a], df.iloc[index_b]
    
    set_a.to_csv('split1.csv')
    set_b.to_csv('split2.csv')

    print '''
    df_result = pd.DataFrame()
    # Model 1
    run output input split1.csv --train
    run output input split2.csv --test output/model

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


