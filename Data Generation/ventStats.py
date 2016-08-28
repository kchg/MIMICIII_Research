import sys
import os
import shutil
from math import log, exp
from collections import defaultdict
import statistics

##add min/max functionality
results = defaultdict(list)
os.chdir("set-a")


mechcount = 0
records = len(os.listdir(os.getcwd())) #number of records

for record in os.listdir(os.getcwd()):
    with open(record) as f:
        content = f.readlines()
        for line in content:
            if (line == "Time,Parameter,Value\n"):
                continue

            sections = line.split(',')
            if sections[1] == 'MechVent':
                mechcount+=1
                break

print("Number of Patients Ventilated: {}".format(str(mechcount)))
    
    
    
