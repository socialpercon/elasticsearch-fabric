#!/bin/bash
for((i=0;i<9;i++))
do
	ssh logstash@192.168.0.17$i python < kill_python.py &
done
