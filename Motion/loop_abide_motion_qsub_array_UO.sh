#!/bin/bash

#PBS -d /home5/flournoy/kids/Motion/ 
#PBS -e /home5/flournoy/ 
#PBS -o /home5/flournoy/ 
#PBS -q short 
#PBS -l nodes=1:ppn=1 
PARAMFILE=abide_motion_parameters.tsv 

line=$(cat $PARAMFILE | head -n $PBS_ARRAYID | tail -n 1)

motion_thresh=$(echo "$line" | cut -f1)
age_l=$(echo "$line" | cut -f2)
age_u=$(echo "$line" | cut -f3)
n=$(echo "$line" | cut -f4)
n_perms=$(echo "$line" | cut -f5)
overwrite=$(echo "$line" | cut -f6)

#PBS -v motion_thresh=${motion_thresh},age_l=${age_l},age_u=${age_u},n=${n},n_perms=100,overwrite=1

/home5/flournoy/kids/Motion/SgeAbideMotion_UO.sh
