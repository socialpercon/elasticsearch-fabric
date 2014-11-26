#!/usr/bin/python
# coding: utf-8
from fabric.api import *
import re

env.parallel = True
#my_hosts = ['logstash@192.168.0.170','logstash@192.168.0.171','logstash@192.168.0.172','logstash@192.168.0.173','logstash@192.168.0.174','logstash@192.168.0.175','logstash@192.168.0.176']
#my_hosts = ['logstash@192.168.0.170','logstash@192.168.0.171','logstash@192.168.0.172','logstash@192.168.0.173','logstash@192.168.0.174','logstash@192.168.0.175']
my_hosts = ['logstash@192.168.0.170','logstash@192.168.0.171','logstash@192.168.0.172','logstash@192.168.0.173','logstash@192.168.0.174','logstash@192.168.0.175']
#my_hosts = ['logstash@192.168.0.170','logstash@192.168.0.171','logstash@192.168.0.172','logstash@192.168.0.173','logstash@192.168.0.174']
#my_hosts = ['logstash@192.168.0.170','logstash@192.168.0.171','logstash@192.168.0.172','logstash@192.168.0.173']
#my_hosts = ['logstash@192.168.0.170','logstash@192.168.0.171','logstash@192.168.0.172']
#my_hosts = ['logstash@192.168.0.171','logstash@192.168.0.172','logstash@192.168.0.173','logstash@192.168.0.174','logstash@192.168.0.175']
#my_hosts = ['logstash@192.168.0.170']
#my_hosts = ['logstash@192.168.0.173','logstash@192.168.0.174','logstash@192.168.0.175']
env.password = ''

#Command

# 제대로 죽었는지 확인
@hosts(my_hosts)
@serial
def shutdown_confirm():
    result = run("ps -ef | grep elasticsearch")
    return result

# elasticsearch 한번에 띄우기 하지만,, 제대로 동작안함
@hosts(my_hosts)
@parallel
def run_case1():
    run("/home/logstash/elasticsearch-1.0.0/bin/elasticsearch -d", pty=False)

# elasticsearch 한번에 띄우기 하지만,, 제대로 동작안함
@hosts(my_hosts)
@serial
def run_cluster_case2():
    result = run("/home/logstash/elasticsearch-3cluster/bin/elasticsearch -d", pty=False)
    return result

@hosts(my_hosts)
@parallel
def run_cluster_case3():
    run("/home/logstash/elasticsearch/elasticsearch-1/bin/elasticsearch -d", pty=False)
    run("/home/logstash/elasticsearch/elasticsearch-2/bin/elasticsearch -d", pty=False)
    run("/home/logstash/elasticsearch/elasticsearch-3/bin/elasticsearch -d", pty=False)

@hosts(my_hosts)
@parallel
def run_cluster_case4():
    run("/home/logstash/elasticsearch4/elasticsearch-1/bin/elasticsearch -d", pty=False)
    run("/home/logstash/elasticsearch4/elasticsearch-2/bin/elasticsearch -d", pty=False)
    run("/home/logstash/elasticsearch4/elasticsearch-3/bin/elasticsearch -d", pty=False)
    run("/home/logstash/elasticsearch4/elasticsearch-4/bin/elasticsearch -d", pty=False)
    
@hosts(my_hosts)
@parallel
def put_head_cluster_case3():
    put("marvel", "/home/logstash/elasticsearch/elasticsearch-1/plugins/", use_sudo=False)
    put("marvel", "/home/logstash/elasticsearch/elasticsearch-2/plugins/", use_sudo=False)
    put("marvel", "/home/logstash/elasticsearch/elasticsearch-3/plugins/", use_sudo=False)

# elasticsearch로 실행된 모든 것을 죽임
@hosts(my_hosts)
def kill():
    put("./kill_application.py", "~/" ,use_sudo=False);
    result = run("python kill_application.py", pty=False)
    run("rm ~/kill_application.py")
    return result

@parallel
@hosts(my_hosts)
def stat():
    run("top -b -n 1 -c -u logstash")
    run("vmstat")
    run("iostat")

# 노드에 인덱스 데이터 날리기 경로를 엄격하게 지정해줘야한다.
@hosts(my_hosts)
def delete_index():
    result = run("rm -rf /DATA1/lavender/data/elasticsearch")
    result = run("rm -rf /DATA2/lavender/data/elasticsearch")
    result = run("rm -rf /DATA3/lavender/data/elasticsearch")
    result = run("rm -rf /DATA1/lavender/data/elasticsearch-1")
    result = run("rm -rf /DATA1/lavender/data/elasticsearch-2")
    result = run("rm -rf /DATA1/lavender/data/elasticsearch-3")
    result = run("rm -rf /DATA2/lavender/data/elasticsearch-1")
    result = run("rm -rf /DATA2/lavender/data/elasticsearch-2")
    result = run("rm -rf /DATA2/lavender/data/elasticsearch-3")
    result = run("rm -rf /DATA3/lavender/data/elasticsearch-1")
    result = run("rm -rf /DATA3/lavender/data/elasticsearch-2")
    result = run("rm -rf /DATA3/lavender/data/elasticsearch-3")
    return result

# TEST CASE 3 elasticsearch 죽이기
def kill_elastic_test3():
    local("curl -XPOST '192.168.0.170:9200/_cluster/nodes/_shutdown'")
    local("curl -XPOST '192.168.0.170:9250/_cluster/nodes/_shutdown'")
    local("curl -XPOST '192.168.0.170:9150/_cluster/nodes/_shutdown'")
  
def sudo_java_run(command):
    sudo(command)

@hosts(my_hosts)
@serial
def setconf():
    variable = run('cat /home/logstash/elasticsearch/elasticsearch-1/config/elasticsearch.yml')
    variable = re.sub('\ndices', '\nindices', variable)
    file = open('elasticsearch.yml', "wb")
    file.write(variable)
    file.close()
    put('elasticsearch.yml','/home/logstash/elasticsearch/elasticsearch-1/config/', use_sudo=False)

    variable = run('cat /home/logstash/elasticsearch/elasticsearch-2/config/elasticsearch.yml')
    variable = re.sub('\ndices', '\nindices', variable)
    file = open('elasticsearch.yml', "wb")
    file.write(variable)
    file.close()
    put('elasticsearch.yml','/home/logstash/elasticsearch/elasticsearch-2/config/', use_sudo=False)
    
    variable = run('cat /home/logstash/elasticsearch/elasticsearch-3/config/elasticsearch.yml')
    variable = re.sub('\ndices', '\nindices', variable)
    #variable = variable + "\nindices.memory.index_buffer_size: 40%"
    file = open('elasticsearch.yml', "wb")
    file.write(variable)
    file.close()
    put('elasticsearch.yml','/home/logstash/elasticsearch/elasticsearch-3/config/', use_sudo=False)

    variable = run('cat /home/logstash/elasticsearch/elasticsearch-4/config/elasticsearch.yml')
    variable = re.sub('\ndices', '\nindices', variable)
    #variable = variable + "\nindices.memory.index_buffer_size: 40%"
    file = open('elasticsearch.yml', "wb")
    file.write(variable)
    file.close()
    put('elasticsearch.yml','/home/logstash/elasticsearch/elasticsearch-4/config/', use_sudo=False)
    # Set the heap size
    #file = open(HOST_HOME + self.es_service_conf + '.dist', "rb")
    #before = file.read()
    #file.close()
    #after = re.sub('set\.default\.ES_HEAP_SIZE=.*', 'set.default.ES_HEAP_SIZE=' + self.es_heap_size, before)

def merge_results(flag):
    if flag=="confirm":
        results = execute(shutdown_confirm)
    elif flag == "case1run":
        results = execute(run_cluster_case1)
    elif flag == "case2run":
        results = execute(run_cluster_case2)
    elif flag == "delete":
        results = execute(delete_elastic_index)
    elif flag == "killall":
        results = execute(kill_elasticsearch)
    elif flag == "case3kill":
        results = execute(kill_elastic_test3)
    elif flag == "stat":
        results = execute(stat)

    print results
