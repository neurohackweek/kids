#!/bin/bash

for motion_thresh in {2..50..2}; do
    for n in {10..300..10}; do 
        for age_l in {6..16}; do 
            for age_gap in 3; do 
                age_u=$(($age_l + $age_gap))
                if [[ ${age_u} -lt 19 ]]; then 
                    echo "Running: motion_thresh: ${motion_thresh}, age range ${age_l} to ${age_u}, sample size ${n}"
                    qsub -d ~/kids/Motion/ -e ~/ -o ~/ -q short -l nodes=1:ppn=1 -v motion_thresh=${motion_thresh},age_l=${age_l},age_u=${age_u},n=${n},n_perms=100,overwrite=1 SgeAbideMotion_UO.sh
                fi
            done
        done
    done
done
