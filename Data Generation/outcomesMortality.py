#/user/bin/python3.4

import os
import shutil
import time
import re
import sys
from math import log, exp

filename = "Outcomes-a.txt"
mortalitylist = []
ihdlist = []

count = 0
with open(filename, "r") as f:
    line = f.readline()
    line = f.readline()
    while(line is not ""):
        if ((count % 100) is 0):
            print("processed {} of 4000".format(count))
        count+=1
        
        elements = line.split(',')
        
        #SAPS score
        #predict mortality: equation from http://clincalc.com/IcuMortality/SAPSII.aspx
        try:
            score = elements[1][0]
            score = float(score)
        except:
            line = f.readline()
            continue
        logit = -7.7631+0.0737*score+0.9971*log(score+1)
        mortality = (exp(logit))/(1+exp(logit))
        mortalitylist.append(mortality)

        #IHD = elements[5][0]
        ihdlist.append(elements[5][0])

        line = f.readline()


print("Average mortality rate: {}".format((sum(mortalitylist)/len(mortalitylist))))

      
    

f.close()
