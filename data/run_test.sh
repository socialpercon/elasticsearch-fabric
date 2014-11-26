#!/bin/bash
for((j=3;j<12;j++))
do
    for((i=0;i<5;i++))
    do
        echo $j $i
        fab -f multi_run_solr.py merge_results:num=$j
    done
    wait
done
