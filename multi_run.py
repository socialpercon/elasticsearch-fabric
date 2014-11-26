#!/usr/bin/python
# coding: utf-8
from fabric.api import *
import re
import threading
import Queue

env.parallel = True
#my_hosts = ['logstash@192.168.0.170','logstash@192.168.0.171','logstash@192.168.0.172','logstash@192.168.0.173','logstash@192.168.0.174','logstash@192.168.0.175','logstash@192.168.0.176','logstash@192.168.0.177','logstash@192.168.0.178']
my_hosts = ['logstash@192.168.0.170','logstash@192.168.0.171','logstash@192.168.0.172','logstash@192.168.0.173','logstash@192.168.0.174','logstash@192.168.0.175']
#my_hosts = ['logstash@192.168.0.170','logstash@192.168.0.171','logstash@192.168.0.172','logstash@192.168.0.173','logstash@192.168.0.174']
#my_hosts = ['logstash@192.168.0.173','logstash@192.168.0.174','logstash@192.168.0.175']
#my_hosts = ['logstash@192.168.0.170','logstash@192.168.0.171','logstash@192.168.0.172','logstash@192.168.0.173']
#my_hosts = ['logstash@192.168.0.170']
#my_hosts = ['root@192.168.0.170','root@192.168.0.171','root@192.168.0.172','root@192.168.0.173','root@192.168.0.174','root@192.168.0.175']
master_hosts = ['logstash@192.168.0.170','logstash@192.168.0.172','logstash@192.168.0.174']
#env.password = 'hello.logstash'
env.password = ''

#Command
command = "java -jar thriftclient-0.0.3-SNAPSHOT-jar-with-dependencies.jar"
file_directory = "/home/logstash/testcode"

#Java
jar_name = 'thriftclient-0.0.3-SNAPSHOT-jar-with-dependencies.jar'
jar_path = "../thrift_example_clients/java/thriftclient/target/" + jar_name

#Docs
docs_path = '../../data/json_data/'


@parallel
@hosts(my_hosts)
def java_run(i):
    with cd(file_directory):
        result = run("%s -docs %s-%d.json" % (command, env.host, i))
    return result

@parallel
@hosts(my_hosts)
def delete_index():
    result = run("curl -XDELETE %s:9200/m6log" % (env.host))
    result = run("curl -XDELETE %s:9200/jetsetter" % (env.host))
    return result
    
@parallel
@hosts(my_hosts)
def multi_java_run(port, i):
    with cd(file_directory):
        result = run("%s -ip localhost -port %s -docs %s-%d.json" % (command, port, env.host, i))
    return result

@parallel
@hosts(my_hosts)
def file_put(number):
    global command
    global file_directory
    
	# file
    #run('mkdir -p ' + file_directory)
    #put(jar_path, file_directory ,use_sudo=False);

    for i in xrange(0,int(number)+1):
        put("%s%s-%d.json" % (docs_path,env.host, i), file_directory, use_sudo=False);
    
def sudo_java_run(command):
    sudo(command)

def merge_results_with_file(num):
    execute(file_put, number=int(num))
    merge_results(num)

def merge_results(num):
    threads = []
    messages = []
    queue = Queue.Queue()
    for i in xrange(1,int(num)+1):
        t = ExecThread(i, queue)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()
    while(not queue.empty()):
        messages.append(queue.get())
    #results = execute(sudo_java_run)
    #timeregex = re.compile('.*\s.*\s.*\s\+\+\+(.*)\-\-\-')
    #timestamps = []
    #for message in messages:
    #    for result in message.itervalues():
    #        match = timeregex.match(result).group(1)
    #        timestamps.append(float(match))

    print messages
    #print timestamps
    #print "avg : %f" % (sum(timestamps,0.0)/len(timestamps))

def multi_merge_results(num):
    threads = []
    messages = []
    queue = Queue.Queue()
    for i in xrange(1,int(num)+1):
        for j in xrange(0,4):
            t = Multi_ExecThread(i, 9500+j, queue)
            threads.append(t)

    for t in threads:
        t.start()
        
    for t in threads:
        t.join()
    while(not queue.empty()):
        messages.append(queue.get())
    #results = execute(sudo_java_run)
    #print messages

class ExecThread(threading.Thread):
    def __init__(self, i, queue):
        threading.Thread.__init__(self)
        self.i = i
        self.queue = queue

    def run(self):
        results = execute(java_run, i=self.i)
        self.queue.put(results)

class Multi_ExecThread(threading.Thread):
    def __init__(self, i, port, queue):
        threading.Thread.__init__(self)
        self.i = i
        self.port = str(port)
        self.queue = queue

    def run(self):
        results = execute(multi_java_run, port=self.port, i=self.i)
        self.queue.put(results)

def resource_monitor():
    threads = []
    messages = []
    queue = Queue.Queue()
    for i in xrange(1,int(num)+1):
        t = ExecThread(i, queue)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()
    while(not queue.empty()):
        messages.append(queue.get())
    #results = execute(sudo_java_run)
    timeregex = re.compile('.*\s.*\s.*\s\+\+\+(.*)\-\-\-')
    timestamps = []
    for message in messages:
        for result in message.itervalues():
            match = timeregex.match(result).group(1)
            timestamps.append(float(match))

    print timestamps
    print "avg : %f" % (sum(timestamps,0.0)/len(timestamps))

class MonitorThread(threading.Thread):
    def __init__(self, i, queue):
        threading.Thread.__init__(self)
        self.i = i
        self.queue = queue

    def run(self):
        results = execute(java_run, i=self.i)
        self.queue.put(results)
