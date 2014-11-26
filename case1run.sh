#!/bin/bash
for((i=0;i<9;i++))
do
	ssh logstash@192.168.0.17$i /home/logstash/elasticsearch-1.0.0/bin/elasticsearch &
done
