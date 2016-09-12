#!/bin/bash

for motion_thresh in {2..50..2}; do
    for n in {10..300..10}; do 
        for age_l in {6..16}; do 
            for age_gap in 3; do 
                age_u=$(($age_l + $age_gap))
                if [[ ${age_u} -lt 19 ]]; then 
                     echo "Running: motion_thresh: ${motion_thresh}, age range ${age_l} to ${age_u}, sample size ${n}"
                   bash SgeAbideMotion_MIT.sh ${motion_thresh} ${age_l} ${age_u} ${n} 10 0
                fi
            done
        done
    done
done
