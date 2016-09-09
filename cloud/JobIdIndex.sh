#!/bin/bash
if [[ $Id -lt 7 ]]; then
	method=1
	if [[ $Id -lt 4 ]]; then
		Set=1
	else
		Set=2
	fi
else
	if [[ $Id -gt 6 ]]; then
	method=2
	if [[ $Id -lt 10 ]]; then
		Set=1
	else
		Set=2
	fi
fi

#for Id in 1..12
method=`echo "($Id-1)/6+1" | bc`
Method=$(($ID-1))

