#!/bin/bash

for motion_thresh in {5..50..5}; do
    for n in {30..100..10}; do 
        echo "${motion_thresh}	6	18	${n}	100	1"
    done
done > abide_motion_parameters.tsv
