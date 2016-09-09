#!/usr/bin/env python

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
parser.add_argument('method', help='The comma-separated names of the classifiers you are using.')
parser.add_argument('-i','--input_dir', help='The directory where the input '
    'files (including the phenotype file) are located.', default=os.getcwd())
parser.add_argument('-o','--output_dir', help='The directory where the output '
    'files should be stored.', default=os.getcwd())
parser.add_argument('-n','--n_iter', type=int, help='The number of iterations '
    'of stratified samples to generate.', default=1)

args = parser.parse_args()

input_dir=args.input_dir.rstrip('/')
output_dir=args.output_dir.rstrip('/')
pheno_file=args.pheno_file
outcome_measure=args.outcome_measure
methods=args.method.split(',')
n_iter=args.n_iter

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
sss = StratifiedShuffleSplit(labels, n_iter, 0.5)

acc = []
repro = []

print 'splitting'
print

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for i, (index_a, index_b) in enumerate(sss):
    set_a, set_b = df.iloc[index_a][[colnames[0],outcome_measure]], df.iloc[index_b][[colnames[0],outcome_measure]]

    for method in methods:
        iter_dir = os.path.join(output_dir,"%s_iteration%s"%(method,i+1))

        if not os.path.exists(iter_dir+'_set1'):
            os.makedirs(iter_dir+'_set1')

        if not os.path.exists(iter_dir+'_set2'):
            os.makedirs(iter_dir+'_set2')

    #set_a.to_csv(iter_dir+'_set1/subs.csv', index=False)
    #set_b.to_csv(iter_dir+'_set2/subs.csv', index=False)
    set_a.to_csv(os.path.join(output_dir, 'iteration%s_set1.csv' %(i+1)), index=False)
    set_b.to_csv(os.path.join(output_dir, 'iteration%s_set2.csv' %(i+1)), index=False)

print 'training models'

for n in range(n_iter):
    for method in methods:
        for i in [1,2]:
            pheno_dir = 'iteration'+str(n+1)+'_set'+str(i)+'/'
            pheno_file = pheno_dir+'subs.csv'
            print "python run.py --pheno_file %s --input_dir %s --train --model_dir %s" % (pheno_file,input_dir,method+'_'+pheno_dir)

print

print 'testing models'
for n in range(n_iter):
    for method in methods:
        pheno_file = 'iteration'+str(n+1)+'_set'
        set_a = method+'_iteration'+str(n+1)+'_set1/'
        set_b = method+'_iteration'+str(n+1)+'_set2/'
        print "python run.py --pheno_file %s --input_dir %s --test --model_dir %s" % (pheno_file+'/set1.csv',input_dir, set_b)
        print "python run.py --pheno_file %s --input_dir %s --test --model_dir %s" % (pheno_file+'/set2.csv',input_dir, set_a)

print
