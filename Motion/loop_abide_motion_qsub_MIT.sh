#!/bin/bash

for motion_thresh in {5..50..5}; do
    for n in {10..50..10}; do 
	for age_l in {6..18..2}; do 
            for age_gap in 4; do 
  		age_u=$(($age_l + $age_gap))
                 if [[ ${age_u} -lt 19 ]]; then 
                      echo "Running: motion_thresh: ${motion_thresh}, age range ${age_l} to ${age_u}, sample size ${n}"
        	      sbatch SgeAbideMotion_MIT.sh ${motion_thresh} ${age_l} ${age_u} ${n} 100 1
fi     
done
done
done
done


