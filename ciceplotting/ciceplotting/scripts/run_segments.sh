#!/bin/bash

EXPERIMENT=$1

NAMELIST="ice_in"
LOGDIR="/fs/homeu3/eccc/cmd/cmdem/fsd001/cicedirs/casesppp7/${EXPERIMENT}/logs"


for segment in 1 2 3 4 5 6 7 8 9 10 11 12; do

    if [ $segment -eq 1 ]; then
        RUNTYPE="initial"
    else
        RUNTYPE="continue"
    fi

    sed -i "s/runtype\s*=\s*'[a-z]*'/runtype        = '${RUNTYPE}'/" $NAMELIST

    echo "Starting segment $segment with runtype = $RUNTYPE"

    jobline=$(./cice.submit)
    job=$(echo "$jobline" | sed 's|^[^0-9]*\([0-9]*\).*$|\1|g')

    if [[ $job =~ ^[0-9]+$ ]]; then
        qstatjob=1
        while [ $qstatjob -eq 1 ]; do
            qstatus=$(qstat $job 2>/dev/null | grep $job | wc -l)
            if [ $qstatus -eq 0 ]; then
                echo "Job $job completed"
                qstatjob=0
            else
                echo "Waiting for $job to complete"
                sleep 60
            fi
        done
    else
        echo "ERROR: no valid job ID found at segment $segment, stopping."
        exit 1
    fi

    echo "Segment $segment done."

    # Find the log file corresponding to this job
    LOGFILE="${LOGDIR}/gx1IMEX.o${job}"

    # Check if log file exists
    if [ ! -f "$LOGFILE" ]; then
        # Try the cice.runlog pattern as fallback
        LOGFILE=$(ls -t ${LOGDIR}/cice.runlog.* 2>/dev/null | head -1)
   fi

    if [ -z "$LOGFILE" ] || [ ! -f "$LOGFILE" ]; then
        echo "WARNING: could not find log file for job $job, stopping to be safe."
        exit 1
    fi

    echo "Checking log file: $LOGFILE"

    # Check for bad departure words
    if grep -qi "bad departure" "$LOGFILE"; then
        echo "ERROR: 'bad departure' found in $LOGFILE at segment $segment, stopping."
        exit 1
    else
        echo "Log check passed, no bad departure words found."
    fi

    echo "Segment $segment done."

done

echo "Full year complete."


