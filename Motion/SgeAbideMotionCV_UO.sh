#!/bin/bash
#########################################################################
# Takes motion threshold, age_l, age_u, n, & n_perms, and submits to run 
# the script on a new worker node!
#########################################################################
# Defines path to the python code you want to run 
Code="/home5/flournoy/kids/Motion/runCVMotionTest.py"
# Defines motion threshold from input 1
echo Running $Code
echo "motion_thresh=${motion_thresh},age_l=${age_l},age_u=${age_u},n=${n},n_perms=${n_perms},overwrite=${overwrite}"
date
/home5/flournoy/miniconda2/envs/kidsPy2/bin/python $Code --fc_file ./abide_fc_data_fisher_z.csv --output_dir cv_output/ --model_dir cv_models/ --mt $motion_thresh --N $n --cvmethod sss --oos_iter $n_perms 
