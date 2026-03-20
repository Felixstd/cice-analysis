#!/bin/bash

# help function
how2use() {
            echo "help:" 
            echo " rename_file.sh -r <filenames> <parts to remove>"
            echo " rename_file.sh -n <filenames> <parts to add>"

            exit 1
}

if [ $# -lt 3 ]; then 
    how2use
    exit 1
fi

Flag=$1 
filenames=$2
arg=$3 

case "$Flag" in 

    -r) 
        for f in ${filenames}.*.nc; 
            do mv "$f" "${f//_${arg}/}"; 
        done;;


    -n)
        for f in ${filenames}.*.nc; do
            mv "$f" "${f/${filenames}./${filenames}_${arg}.}";
        done;;

esac

