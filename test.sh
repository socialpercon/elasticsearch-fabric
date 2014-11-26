#!/bin/bash
# 한 개의 노드에 elasticsearch가 여러개 있다고 가정할 경우 아래 스크립트 사용
for((i=1;i<11;i++))
do
    curl -XDELETE '192.168.0.170:9200/jetsetter'
    curl -XDELETE '192.168.0.170:9250/jetsetter'
    curl -XDELETE '192.168.0.170:9150/jetsetter'
    sleep 5
    fab -f multi_run.py multi_merge_results:num=1
done

# 한 개의 노드에 elasticsearch가 하나만 있다고 가정할 경우 아래 스크립트 사용
#for((i=1;i<10000;i++))
#do
#    curl -XDELETE '192.168.0.170:9200/jetsetter'
#    sleep 5
#    fab -f multi_run.py merge_results:num=1
#done

# 한 개의 노드에 elasticsearch가 하나만 있다고 가정하고 프로세스가 여러개 일때 아래 스크립트 사용
#for((i=1;i<11;i++))
#do
#    curl -XDELETE '192.168.0.170:9200/jetsetter'
#    fab -f multi_run.py merge_results:num=3
#done
