#!/bin/bash

#PBS -d /home5/flournoy/kids/Motion/ 
#PBS -e /home5/flournoy/ 
#PBS -o /home5/flournoy/ 
#PBS -q short 
#PBS -l nodes=1:ppn=4 
PARAMFILE=abide_motion_parameters.tsv 

line=$(cat $PARAMFILE | head -n $PBS_ARRAYID | tail -n 1)

export motion_thresh=$(echo "$line" | cut -f1)
export age_l=$(echo "$line" | cut -f2)
export age_u=$(echo "$line" | cut -f3)
export n=$(echo "$line" | cut -f4)
export n_perms=$(echo "$line" | cut -f5)
export overwrite=$(echo "$line" | cut -f6)

#motion_thresh=${motion_thresh},age_l=${age_l},age_u=${age_u},n=${n},n_perms=100,overwrite=1

#PBS -V 

/home5/flournoy/kids/Motion/SgeAbideMotionCV_UO.sh
