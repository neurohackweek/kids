import argparse
import pandas as pd
from sklearn.cross_validation import StratifiedShuffleSplit
import numpy as np
import os
import sys

parser = argparse.ArgumentParser(description='NPAIRS Framework Runner')
parser.add_argument('pheno_file', help='File containing the participant'
    'information for the analysis that will be run. This is a CSV with the'
    'participant id in the first column and the dependent variable and '
    'regressors of no interest in the remaining columns.')
parser.add_argument('outcome_measure', help='The outcome measure you are '
    'interested in predicting.')
parser.add_argument('-i','--input_dir', help='The directory where the input '
    'files (including the phenotype file) are located.', default=os.getcwd())
parser.add_argument('-o','--output_dir', help='The directory where the output '
    'files should be stored.', default=os.getcwd())

args = parser.parse_args()

input_dir=args.input_dir.rstrip('/')
output_dir=args.output_dir.rstrip('/')
pheno_file=os.path.join(args.input_dir,args.pheno_file)
outcome_measure=args.outcome_measure

if not os.path.isfile(pheno_file):
    print("Could not find pheno file %s"%(pheno_file))
    sys.exit(1)

if not os.path.isdir(input_dir):
    print("Could not find input directory %s"%(input_dir))
    sys.exit(1)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

df = pd.read_csv(pheno_file)
colnames = df.keys()

if outcome_measure not in colnames:
    print("Could not find %s in file %s"%(outcome_measure, pheno_file))
    sys.exit(1)

labels = [ '.'.join([str(df[key].iloc[i]) for key in colnames[1:]]) for i in range(len(df))]
sss = StratifiedShuffleSplit(labels, 3, 0.5)

acc = []
repro = []

for i, (index_a, index_b) in enumerate(sss):
    print
    print 'iteration %s' % (i+1)
    set_a, set_b = df.iloc[index_a][[colnames[0],outcome_measure]], df.iloc[index_b][[colnames[0],outcome_measure]]
    
    set_a.to_csv(os.path.join(output_dir,'set1_iteration%s.csv' % (i+1)), index=False)
    set_b.to_csv(os.path.join(output_dir,'set2_iterations%s.csv' % (i+1)), index=False)

    #os.system("python run.py split1.csv -i %s --train" % output_dir)

    #os.system("python run.py split2.csv -o model1 --test")

    # train on second half, test on first half
    #os.system("python run.py split2.csv -o model2 --train")
    #os.system("python run.py split1.csv -o model2 --test")

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


