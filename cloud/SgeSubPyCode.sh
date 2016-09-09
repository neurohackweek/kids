#!/bin/bash
#########################################################################
# Takes input, output, and python code file and runs the python script
# with input and output as input arguments. The code input is necessary, 
# but the others are not. 
#########################################################################
# Define qsub options:
# Use current working directory
#$ -cwd
# Combine job and error logs
#$ -j y
#$ -V
# Defines the python code you want to run on a new worker node from input 1
Code=$1
# Defines the input argument needed (if any) for the code to run from input 2
Input=$2
# Defines the output argument needed (if any) for the code to run from input 3
Output=$3
echo Running $Code on $Input
date
python $Code $Input $Output