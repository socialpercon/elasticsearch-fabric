#!/usr/bin/python
# coding: utf-8
from fabric.api import *
import re

env.parallel = True
my_hosts = ['logstash@192.168.0.170','logstash@192.168.0.171','logstash@192.168.0.172','logstash@192.168.0.173','logstash@192.168.0.174','logstash@192.168.0.175','logstash@192.168.0.176','logstash@192.168.0.177','logstash@192.168.0.178']
#my_hosts = ['logstash@192.168.0.170','logstash@192.168.0.171']
env.password = ''

#Command
command = "java -jar thriftclient-0.0.1-SNAPSHOT-jar-with-dependencies.jar"
file_directory = "~/testcode"

#Java
jar_name = 'thriftclient-0.0.1-SNAPSHOT-jar-with-dependencies.jar'
jar_path = "./target/" + jar_name

#Docs
docs_path = '../../data/json_data/'

@hosts(my_hosts)
def java_run():
    global command
    global file_directory
    
	# file
    run('mkdir -p ' + file_directory)
    put(jar_path, file_directory ,use_sudo=False);

    for i in xrange(1,2):
        put("%s%s-%d.json" % (docs_path,env.host, i), file_directory, use_sudo=False);
    i=1
    with cd(file_directory):
        result = run("%s -docs %s-%d.json" % (command, env.host, i))
    return result


  
def sudo_java_run(command):
    sudo(command)

def merge_results_with_file():
    execute(file_put)
    merge_results()

def merge_results():
    results = execute(java_run)
    #results = execute(sudo_java_run)
    timeregex = re.compile('.*\s.*\s.*\s\+\+\+(.*)\-\-\-')
    timestamps = []
    for result in results.itervalues():
        match = timeregex.match(result).group(1)
        timestamps.append(float(match))

    print timestamps
    print "avg : %f" % (sum(timestamps,0.0)/len(results))
