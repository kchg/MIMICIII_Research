#/user/bin/python3.4

#gendata.py
#September 2016
#This program queries a MIMIC database and generates a number of data files for
#icustays in ICU, and filters the data based on itemids of chart and lab events.
#Data is placed in a folder named set-a, with each file containing one icustay,
#with the file name as the icustay_id.

import psycopg2
import psycopg2.extras
import os
import shutil
import time
import re
import sys
from genHelper import *
import datetime
from datetime import timedelta


print (items.keys())

##print messages for patients
verbose = 1

conn = connect()

#define dictionary cursor to work with (keyed on column name)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) #results in dictionary form

#create directory to place data files
if not os.path.exists("set-a"):
    os.makedirs("set-a")
else: #remove directory
    try:
        shutil.rmtree("set-a", ignore_errors=True)
        time.sleep(1)
        os.makedirs("set-a")
    except:
        print("Folder set-a could not be removed, make sure any programs using set-a are closed, including python shells.")
        sys.exit()


print ("Processing Data...")

#create list of item ids to accept (in genHelper)
ids = list(items.keys())
for index, x in enumerate(ids): ids[index] = int(x)

# Get the ICUStays and details List
cur.execute(open('genDataScripts/validICUStays.sql', 'r').read())
ICU = cur.fetchall()



#######Start Processing Each Subject##################
count = 0 #track how many subjects processed
skipped = 0
num_stays = len(ICU)

for icustay in ICU:
    icustay_id = icustay['icustay_id']
    filename = "set-a/{0}.txt".format(icustay_id)

    #create list of item ids to accept (in genHelper)
    ids = list(items.keys())
    for index, x in enumerate(ids): ids[index] = int(x)
    for index, x in enumerate(URINEIDS): URINEIDS[index] = int(x)
    
    
    ## Time Series Variables
    cur.execute(open('genDataScripts/timeSeriesVariables.sql', 'r').read().format(icustay_id), (ids, URINEIDS))
    result = cur.fetchall()
    
    if cur.rowcount is 0:
        print("skipping {}, no data".format(icustay_id))
        count+=1
        skipped+=1
        continue
    
    with open(filename, 'w') as f:
        f.write("Time,Parameter,Value\n")
        f.write("00:00,RecordID,{0}\n".format(icustay_id))
        f.write("00:00,Age,{0}\n".format(int(icustay['age']) if int(icustay['age']) is not None else '-1'))
        f.write("00:00,Gender,{0}\n".format(int(icustay['gender_num'])))
        f.write("00:00,Height,{0}\n".format(icustay['height_first'] if icustay['height_first'] is not None else '-1'))
        f.write("00:00,ICUType,{0}\n".format(icustay['icutype']))
        f.write("00:00,Weight,{0}\n".format(icustay['weight_first'] if icustay['weight_first'] is not None else '-1'))
        f.write("00:00,MechVent,{0}\n".format(icustay['mechvent']))

        
        initialTime = result[0]['charttime']
        for row in result:
            ##Conversions
            #MechVent
            if(row['itemid'] in (722,720,227565,467,468,469)): row['valuenum'] = 1

            #FiO2
            if(row['itemid'] in (223835, 3420)): row['valuenum'] = float(row['valuenum'])/100.0
            #Convert date
            time = (row['charttime']) #datetime object
            delta = (time-initialTime).total_seconds()
            
            #only count first 48 hours
            if((delta/3600) > 48): break;
            
            m,s = divmod(delta, 60)
            h,m = divmod(m, 60)
            #zfill pads with 0 if necessary, int removes the floating point
            outputTime = "{}:{}".format(str(int(h)).zfill(2), str(int(m)).zfill(2))

            #ignore strings
            p = re.compile('\d+(\.\d+)?')
            v = str(row['valuenum'])
            if((p.match(v) is None)):
                s = str(outputTime) + "," + str(label(str(row['itemid']))) + "," + str(row['valuenum']) + "\n"
            #Ignore empty measurements
            elif(str(row['valuenum']) != ""):
                if(row['itemid'] in URINEIDS):
                   s = str(outputTime) + "," + "Urine" + "," + str(row['valuenum']) + "\n"
                else: s = str(outputTime) + "," + str(label(str(row['itemid']))) + "," + str(row['valuenum']) + "\n"
                f.write(s)
                
        count +=1
        if ((count % 500) is 0):
            print("Processed {} records out of {}...".format(count, num_stays))


print("Done.")
print("Results: {} subject files created, {} subjects skipped.".format(count-skipped, skipped))
os.chdir("..")


conn.close()







