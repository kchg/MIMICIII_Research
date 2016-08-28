import sys
import os
import shutil
from math import log, exp
from collections import defaultdict
import statistics

##add min/max functionality
results = defaultdict(list)
os.chdir("set-a-new")


count= 0;
records = len(os.listdir(os.getcwd())) #number of records

for record in os.listdir(os.getcwd()):
    if(count % 1000 is 0):
        print("Processed {} of {} records...".format(count, records))
    count += 1
    with open(record) as f:
        content = f.readlines()
        for line in content:
            if (line == "Time,Parameter,Value\n"):
                continue

            sections = line.split(',')
            results[sections[1]].append(sections[2])

##for each feature, print out the stats
for key in sorted(results.keys()):
    if (key is "Parameter"): continue
    values = list(map(float, results[key]))
    print("Feature {}:".format(key))
    print("Size:",len(values))
    print("Min:",min(values))
    print("Max:",max(values))
    print("Average:{0:0.2f}".format(statistics.mean(values)))
    print("Median:",statistics.median(values))
    print('\n')
    
    
    
