#!/bin/bash

for motion_thresh in {5..80..5}; do
    for n in {10..100..10}; do 
    	echo "Running: motion_thresh: ${motion_thresh}, age range 6 to 18, sample size ${n}"
        sbatch SgeAbideMotion_MIT.sh ${motion_thresh} 6 18 ${n} 100 1
    done
done
