#!/bin/bash

for motion_thresh in {18..50..2}; do
    for n in {10..300..10}; do 
        for age_l in {6..16}; do 
            for age_gap in 3; do 
                age_u=$(($age_l + $age_gap))
                if [[ ${age_u} -lt 19 ]]; then 
                    echo "${motion_thresh}	${age_l}	${age_u}	${n}	100	1"
                fi
            done
        done
    done
done > abide_motion_parameters.tsv
