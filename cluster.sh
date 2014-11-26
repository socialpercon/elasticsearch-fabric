#!/bin/sh
rm ./cluster3_node2.txt
for((i=1;i<20;i++))
do
    curl -XGET 'http://localhost:8983/solr/admin/collections?action=DELETE&name=collection1'
    curl 'http://localhost:8983/solr/admin/collections?action=CREATE&name=collection1&numShards=2&maxShardsPerNode=100&replicationFactor=2&collection.configName=myconf'
    stdbuf -oL java -Durl=http://localhost:8983/solr/collection1/update -Dtype=text/json -jar post.jar solr.json &>> ./cluster3_node2.txt
done

