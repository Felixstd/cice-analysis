#!/bin/bash

NAMELIST="ice_in"

for segment in 1 2 3 4 5 6 7 8 9 10 11 12; do
	
	if [ $segment -eq 1 ]; then 
		RUNTYPE="initial"
	else
		RUNTYPE="continue"
	fi 

	sed -i "s/runtype\s*=\s*'[a-z]*'/runtype        = '${RUNTYPE}'/" $NAMELIST

	echo "Starting segment $segment with runtype = $RUNTYPE"

	# Capture the job ID from qsub
	jobid=$(./cice.submit)
	echo "Submitted job $jobid, waiting..."

	# Poll until job is no longer in the queue
	while qstat $jobid 2>/dev/null | grep -q $jobid; do
   		sleep 300
	done
	
	echo "Segment $segment done"
done 


