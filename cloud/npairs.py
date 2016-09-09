#!/usr/bin/env python

import argparse, os, sys, commands, re, template_qsub
from sklearn.cross_validation import StratifiedShuffleSplit
import pandas as pd
import numpy as np

# generate argument parser object
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

# read in commandline arguments
args = parser.parse_args()

# set variables based on commandline inputs
input_dir=args.input_dir.rstrip('/')
output_dir=args.output_dir.rstrip('/')
pheno_file=args.pheno_file
outcome_measure=args.outcome_measure
methods=args.method.split(',')
n_iter=args.n_iter

# check phenotype file exists
if not os.path.isfile(pheno_file):
    print("Could not find pheno file %s"%(pheno_file))
    sys.exit(1)

# check image input directory exists
if not os.path.isdir(input_dir):
    print("Could not find input directory %s"%(input_dir))
    sys.exit(1)

# make output directory if doesn't already exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# read in phenotype file
df = pd.read_csv(pheno_file)

# check that the outcome measure is a column in the phenotype file
colnames = df.keys()
if outcome_measure not in colnames:
    print("Could not find %s in file %s"%(outcome_measure, pheno_file))
    sys.exit(1)

# create dot product of labels
labels = [ '.'.join([str(df[key].iloc[i]) for key in colnames[1:]]) for i in range(len(df))]

# create stratified 2fold splits of data
sss = StratifiedShuffleSplit(labels, n_iter, 0.5)

# iterate over the number of iterations
for i, (index_a, index_b) in enumerate(sss):

    # split into 2 sets based on results of stratified splits
    set_a, set_b = df.iloc[index_a][[colnames[0],outcome_measure]], df.iloc[index_b][[colnames[0],outcome_measure]]

    # create appropriate directory structure
    for method in methods:
        iter_dir = os.path.join(output_dir,"%s_iteration%s"%(method,i+1))

        if not os.path.exists(iter_dir+'_set1'):
            os.makedirs(iter_dir+'_set1')

        if not os.path.exists(iter_dir+'_set2'):
            os.makedirs(iter_dir+'_set2')

    # save out subject lists for each iteration
    set_a.to_csv(os.path.join(output_dir, 'iteration%s_set1.csv' %(i+1)), index=False)
    set_b.to_csv(os.path.join(output_dir, 'iteration%s_set2.csv' %(i+1)), index=False)

# generate qsub script
qsub = template_qsub.get_qsub_file(input_dir, output_dir, n_iter,methods)
filename = 'run_jobs.qsub'
with open(filename,'w') as textFile:
    textFile.write(qsub)

# submit qsub script
out = commands.getoutput('qsub %s' % filename)

# check whether script was successfully submitted
if re.search(confirm_str, out) == None:
    err_msg = 'Error submitting job to queue')
    raise Exception(err_msg)
