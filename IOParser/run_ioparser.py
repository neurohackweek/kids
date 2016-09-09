#!/usr/bin/env python
import argparse
import os
import sys
import urllib
import pandas as pd
import subprocess
import glob
import nibabel as nib
import numpy as np
import sklearn
from nilearn.input_data import NiftiMasker
import nilearn
import csv

######################################
#Functions
######################################

def write_csv(listfile,filename):

	print('Writing to csv file:', filename)
	with open(filename, 'w') as f:
		f.writelines(listfile)

	return

#####################################

def get_features_mtx(pheno_file, mask_img,output_path):
# get the feature matrix X, true values Y, mask image
	missing_data=['subjects\n']
	fnames=[]
	phenos = pd.read_csv(pheno_file,index_col=0)

	print('Parsing files')
	for ss in phenos.index:
		try:
			f = glob.glob(os.path.join(input_dir,'*%s*.nii.gz' % ss))[0]
			fnames.append(f)
		except:
			missing_data.append(str(ss)+'\n')


	trimmed_phenos = phenos[~phenos.index.isin(missing_data)]
	Y=trimmed_phenos['DX_GROUP'].values # labels or diagnosis group or Y for classifier

	mask=nib.load(mask_img)
	masker=NiftiMasker(mask_img=mask)

	print('Generating feature matrix  nsubjects x voxels')
	# only brain functional voxels
	X=masker.fit_transform(fnames)

	write_csv(missing_data,os.path.join(output_path,'missing_data.csv'))
	return X,Y,masker






######################################
######################################

dtype=['train', 'test']
test_model=['svm']

def run(command, env={}):
    process = Popen(command, stdout=PIPE, stderr=subprocess.STDOUT,
        shell=True, env=env)
    while True:
        line = process.stdout.readline()
        line = str(line, 'utf-8')[:-1]
        print(line)
        if line == '' and process.poll() != None:
            break


# Get arguments
parser = argparse.ArgumentParser(description='ABIDE Classifier Model')
parser.add_argument('--pheno_file', help='File containing the participant'
    'information for the analysis that will be run. This is a CSV with the'
    'participant id in the first column, the diagnosis in the'
    'second column.', required=True)
parser.add_argument('--input_dir', help='Directory with subject files', required=True)
parser.add_argument('--output_dir', help='Directory to contain output i.e. model weights and  model details',required=True)
parser.add_argument('--mask', help='Mask for non-zero brain tissue. Needs complete path',required=True)
parser.add_argument('--train', action='store_true')
parser.add_argument('--test', action='store_true')
parser.add_argument('--model_wts', help='3D NII image with weights for each voxel feature')
parser.add_argument('--classfr', help='Type of classifier')

# get the command line arguments
args = parser.parse_args()

# Check for correct and sufficient arguments
if args.train:
	print('training data')

if args.test:
	if args.model_wts:
		model_wts=nib.load(args.model_wts)
		model_img=model_wts.get_data()
	else:
		parser.error('Need Model Wt. Image')

if args.train is None and args.test is None:
	parser.error('Enter flag for data: --train or --test')

if args.mask:
		mask_img=args.mask
else:
		parser.error('Need Mask Image')

# check for output directory
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)
output_path=os.path.abspath(args.output_dir)


#########################################
#Read input directory
input_dir = args.input_dir


# Get X or voxel wise features and Y for the classifier function in the sci-kit learn format
#subj_ids = np.genfromtxt(args.pheno_file, usecols=0, delimiter=',', skip_header=1, dtype='str')
X,Y,masker = get_features_mtx(args.pheno_file,mask_img,output_path)

#########################################
