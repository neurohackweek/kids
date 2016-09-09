#!/bin/bash
#########################################################################
# Takes input and output code file and runs the classifier 2 python script
# with input and output as input arguments. 
#########################################################################
# Define qsub options:
# Use current working directory
#$ -cwd
# Combine job and error logs
#$ -j y
#$ -V
# Defines the input argument needed (if any) for the code to run from input 2
Input=$1
# Defines the output argument needed (if any) for the code to run from input 3
Output=$2
# Define path to the training classifier code
Train2=/path/to/training/code
# Define path to the testing classifier code
Test2=/path/to/testing/code
echo --------------------------------
echo Running classifier 2 training on $Input
date
python $Train1 $Input $Output
echo --------------------------------
echo Running classifier 2 testing on $Input
date
python $Test1 $Input $Output