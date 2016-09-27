#!/bin/bash

for motion_thresh in {2..50..2}; do
    for n in {30..100..10}; do 
        echo "${motion_thresh}	6	18	${n}	500	1"
    done
done > abide_motion_parameters.tsv
