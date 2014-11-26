#!usr/bin/python
# coding: utf-8
import re
import sys
import os

def generator_file(filename, target):
    frontback = re.compile(r"(\[.*?)( .*)")
    path = os.getcwd()
    try:
        f = open(filename, 'r')
        parsing = open(target, 'w')
    except (IOError, OSError), e:
        print "error: %s" %e
    try:    
        while True:
            chunk = f.readline()
            if chunk:
                match = frontback.match(chunk).group(1,2)
                front = match[0]
                back = match[1]
                parsing.write("%s\n" % back)
            else:
                break

    finally:
        f.close()
        parsing.close()


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        generator_file(sys.argv[1], sys.argv[2])
    else:
        print "failed : wrong argument"
