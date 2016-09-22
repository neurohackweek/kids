#!/bin/bash

for motion_thresh in {5..80..5}; do
    for n in {10..100..10}; do 
        echo "${motion_thresh}	6	18	${n}	100	1"
    fi
    done
done > abide_motion_parameters.tsv
