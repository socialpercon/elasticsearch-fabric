import time
import json
import uuid
import sys
import re

def json_generator(filename, limit, target):
    hline = "atimestamp mode msg"
    header = [word for word in hline.split(' ') if len(word) > 0]
    print header
    file_handle = open('./mce.log', 'rb')
    reg = re.compile(u'\[(.*?)\]\[(.*?)\] : (.*)')
    writer = open("./%s.json" % filename, 'w')
    counter = 0

    print "prepare bulk"
    start = time.time()
    print start
    while(True):
        file_handle.seek(0)
        for row in file_handle:
            try:
                dict = {}
		dict['id'] = target + str(uuid.uuid4())
                match = reg.match(row).group(1,2,3)
                for i in xrange(len(header)):
                    dict[header[i]] = match[i]
                writer.write(json.dumps(dict)+",\n")
                counter += 1
                if counter >= limit: 
                    break
            except:
                pass
        if counter >= limit: 
            break
    end = time.time() - start
    print "count : %d time : %.02f sec" % (counter, end)
    print "%.02f rows per sec" % (counter / end)

if __name__ == "__main__":
    args = sys.argv
    print args[1] + args[2] + args[3]
    if len(args) >= 3:
        json_generator(args[1], int(args[2]), args[3])
    else:
        print "failed : wrong argument"
