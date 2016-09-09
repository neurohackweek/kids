#!/bin/bash
#########################################################################
# Takes motion threshold, age_l, age_u, n, & n_perms, and submits to run 
# the script on a new worker node!
# To use: 
# qsub SgeAbideMotion.sh motion_thresh age_l age_u n n_perms
#########################################################################
# Define qsub options:
# Use current working directory
#$ -cwd
# Combine job and error logs
#$ -j y
#$ -V
# Defines path to the python code you want to run 
Code="~/abide_motion_wrapper.py"
# Defines motion threshold from input 1
motion_thresh=$1
age_l=$2
age_u=$3
n=$4
n_perms=$5
echo Running $Code
date
python $Code $motion_thresh $age_l	$age_u $n $n_perms