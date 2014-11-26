#!/bin/bash
for((j=0;j<20;j++))
do
    for((i=0;i<7;i++))
    do
        python iris_generator_solr.py 192.168.0.17$i-$j 100000 192168017$i-$j
    done
    wait
done
