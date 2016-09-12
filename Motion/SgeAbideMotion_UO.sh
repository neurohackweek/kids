#!/bin/bash
#########################################################################
# Takes motion threshold, age_l, age_u, n, & n_perms, and submits to run 
# the script on a new worker node!
# To use: 
# srun SgeAbideMotion.sh motion_thresh age_l age_u n n_perms
#########################################################################
# Defines path to the python code you want to run 
Code="/home5/flournoy/kids/Motion/abide_motion_wrapper.py"
# Defines motion threshold from input 1
echo Running $Code
date
/home5/flournoy/miniconda2/envs/kids/bin/python $Code $motion_thresh $age_l $age_u $n $n_perms $overwrite
