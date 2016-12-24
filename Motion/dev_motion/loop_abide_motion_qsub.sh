#!/bin/bash


for motion_thresh in $(seq .05 0.05 1);do
    for n in {10..20..10}; do 
    	echo "Running: motion_thresh: ${motion_thresh}, age range 6 to 18, sample size ${n}"
        sbatch SgeAbideMotion.sh ${motion_thresh} 6 18 ${n} 100 1
    done
done
