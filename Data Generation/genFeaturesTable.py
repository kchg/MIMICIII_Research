##Kevin Chiang
##August 30, 2016
##This script takes a set of patient data files and creates a feature matrix containing the
##first, last, highest, lowest, median, and frequency counts of each feature.
##The rows are patients and the columns are features

import sys
import os
import shutil
from math import log, exp
from collections import defaultdict
import statistics
import csv

## What you want your csv file to be named
csvname = "features.csv"

## The location of the data files
data_folder = "set-a"


def CreateHeaderRow(csvfile):
    features = ['Albumin','ALP','ALT','AST','Bilirubin','BUN','Cholesterol',
                'Creatinine','DiasABP','FiO2','GCS','Glucose','HCO3','HCT','HR',
                'K','Lactate','Mg','MAP','MechVent','Na','NIDiasABP','NIMAP','NISysABP','PaCO2',
                'PaO2','pH','Platelets','RespRate','SaO2','SysABP','Temp',
                'TroponinI','TroponinT','Urine','WBC','Weight']
    ##For each feature, have first, last, highest, lowest, median, and frequency columns
    ##Individual features: RecordID, Age, Gender, Height, ICUType
    fieldnames = ['RecordID','Age','Gender','Height','ICUType']
    for feature in features:
        fieldnames.append(feature+'First')
        fieldnames.append(feature+'Last')
        fieldnames.append(feature+'Highest')
        fieldnames.append(feature+'Lowest')
        fieldnames.append(feature+'Median')
        fieldnames.append(feature+'Frequency')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    return writer
    
    
with open(csvname, 'w', newline='') as csvfile:
    writer = CreateHeaderRow(csvfile)
    os.chdir(data_folder)
    count= 0;
    records = len(os.listdir(os.getcwd())) #number of records
    for record in os.listdir(os.getcwd()):
        if(count % 1000 is 0):
            print("Processed {} of {} records...".format(count, records))
        count += 1
        
        with open(record) as f:
            results = defaultdict(list) ##defaultdict used for min/max
            content = f.readlines()
            for line in content:
                if (line == "Time,Parameter,Value\n"): continue
                sections = line.split(',')
                results[sections[1]].append(sections[2])
                
            insertRow = {}
            
            ## iterate through the features
            for key in results.keys():
                values = list(map(float, results[key]))
                if key in ('RecordID','Age','Gender','Height','ICUType'):
                    insertRow[key] = values[0]
                else:
                    insertRow[key+'First'] = values[0]
                    insertRow[key+'Last'] = values[-1]
                    insertRow[key+'Highest'] = max(values)
                    insertRow[key+'Lowest']= min(values)
                    insertRow[key+'Median']= statistics.median(values)
                    insertRow[key+'Frequency']=len(values)

            ## write the row    
            writer.writerow(insertRow)
            
            insertRow.clear()
            results.clear()

print('Done')
