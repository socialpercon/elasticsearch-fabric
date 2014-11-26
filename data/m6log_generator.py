import sys
import time
import random

def m6log_generator(filename, target):
    reader = open(filename, 'rb')
    writer = open(target, 'a')
    counter = 0
    print "prepare"
    start = time.time()
    while(True):
        reader.seek(0)
        for row in reader:
            try:
                now = time.localtime()
                s = "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
                writer.write("["+s+"] "+row)
                counter=counter+1
                if (counter % random.randrange(3,8)) == 0:
                    time.sleep(1)
            except:
                return
    end = time.time() - start

if __name__ == "__main__":
    args = sys.argv
    if len(args) >= 2:
        m6log_generator(args[1], args[2])
    else:
        print "failed : wrong argument"
