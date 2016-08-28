#/user/bin/python3.4

#gendata.py
#February 2016
#This program queries a MIMIC database and generates a number of data files for
#patients in ICU, and filters the data based on itemids of chart and lab events.
#Data is placed in a folder named set-a, with each file containing one patient,
#with the file name as the patient id.

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




##print messages for patients
verbose = 1

conn = connect()

#define dictionary cursor to work with (keyed on column name)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) #results in dictionary form

#generate subjects 
SUBJECTS_QUERY = "SELECT \
  patients.subject_id \
FROM \
  mimiciii.patients limit 6000;"

try: cur.execute(SUBJECTS_QUERY)
except:
    print ("Couldn't execute subjects query")
    sys.exit()
subjects = cur.fetchall()

num_subjects = cur.rowcount

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

os.chdir("set-a")
print ("Processing Data...")

#create list of item ids to accept (in genHelper)
ids = list(items.keys())
for index, x in enumerate(ids): ids[index] = int(x)


#######Start Processing Each Subject##################
count = 0 #track how many subjects processed
skipped = 0
original_subjects = num_subjects
for subject_id in subjects:
    subject_id=subject_id[0] #convert from list of list


    last_id = 0
    last_stay_intime = 0
    #have only last icustay
    numhadmquery = "select subject_id, hadm_id, admittime, deathtime \
           from mimiciii.admissions where subject_id = {} order by admittime;".format(subject_id)
    cur.execute(numhadmquery)
    hadm_ids = cur.fetchall()
    #if there's more than one icustay
    #get the last icu stay id
    if(len(hadm_ids) is 0):
        if(verbose): print("Could not process subject", subject_id, ": no icustay_ids\n")
        continue
        
    last_id = hadm_ids[-1]
    last_hadm_id = last_id['hadm_id']

        
    if cur.rowcount is not 1:
        print("subject {}:".format(subject_id))
        cur.execute(ITEM_QUERY_CUSTOM_DATE, (subject_id, last_hadm_id, ids, subject_id, last_hadm_id, ids, subject_id, last_hadm_id))
    else:
        cur.execute(ITEM_QUERY, (subject_id, ids, subject_id, ids, subject_id)) #execute with arguments

########################################
########################################

        
    result = cur.fetchall()
    if cur.rowcount is 0:
        if(verbose): print("Skipping subject {}: No data\n".format(subject_id))
        continue

    initialTime = result[0]['charttime']

#################################################
    

    #stay over 48 hours
    IN_DATE_QUERY = "select admittime \
    from mimiciii.admissions \
    where subject_id = {} AND hadm_id = {};".format(subject_id, last_hadm_id)
    cur.execute(IN_DATE_QUERY)
    
    in_date = cur.fetchone()
    if (cur.rowcount is 0): continue
    else: in_date = in_date['admittime']
    
    OUT_DATE_QUERY = "select dischtime \
    from mimiciii.admissions \
    where subject_id = {} AND hadm_id = {};".format(subject_id, last_hadm_id)
    cur.execute(OUT_DATE_QUERY)

    out_date = cur.fetchone()
    if (cur.rowcount is 0): continue
    else: out_date = out_date['dischtime']

    if(out_date is None or in_date is None):
        if(verbose): print("missing date data: skipping\n")
        continue
    
    los = (out_date - in_date).days

    if (los < 2):
        if(verbose): print("length of stay too short: skipping\n")
        continue

    #########################################
    #Skip Newborns
    #Patient's age.
    sql = "SELECT patients.dob \
           FROM mimiciii.patients \
           WHERE subject_id = (%s);"
    cur.execute(sql,(subject_id,))
    if (cur.rowcount is 0):
        if(verbose): print ("Skipping id {}: no age".format(subject_id))
        continue

    ret = cur.fetchone()
    age = getAge(initialTime, ret['dob'])

    ##Skip newborns (for now)
    if (age < 15): continue


    ##check if icutype is valid
    # Access Patient's ICU Type.
    sql = "SELECT first_careunit \
           FROM mimiciii.icustays \
           WHERE subject_id = (%s) AND hadm_id = {};".format(last_hadm_id)
    cur.execute(sql,(subject_id,))
    ret = cur.fetchall()
    if cur.rowcount is 0:
        icutype = -1
    else:
        icutype = ret[-1]
        if icutype is None:
            icutype = -1
        else:
            icutype = icutype[0]
            if (icutype == "CCU"):
                icutype = 1
            elif (icutype == "CSRU"):
                icutype = 2
            elif (icutype == "MICU"):
                icutype = 3
            elif (icutype == "SICU"):
                icutype = 4
            else: continue



    ######################Start Writing#############################

    filename = "{0}.txt".format(subject_id)
    with open(filename, "w") as f:
        num_subjects -= 1

        f.write("Time,Parameter,Value\n")
        f.write("00:00,RecordID,{0}\n".format(subject_id))


        f.write("00:00,Age,{0}\n".format(age))

        #Patient's gender.
        sql = "SELECT patients.gender \
               FROM mimiciii.patients \
               WHERE subject_id = (%s);"
        cur.execute(sql,(subject_id,))
        ret = cur.fetchone()
        f.write("00:00,Gender,{0}\n".format(translateGender(ret['gender'])))


        # Access Patient's height.
        sql = "SELECT chartevents.valuenum, chartevents.itemid, chartevents.subject_id \
               FROM mimiciii.chartevents \
               WHERE subject_id = {} AND chartevents.itemid in(920, 226730) AND chartevents.valuenum IS NOT NULL  \
               ORDER BY chartevents.charttime;".format(subject_id)
        cur.execute(sql)

        # Write -1 if there was no height.
        if(cur.rowcount == 0):
            f.write("00:00,Height,-1\n")
        
        # If there was a height returned, ensure it is in centimeters.
        else:
            ret = cur.fetchall() #for this data set, use the last height
            ret = ret[-1]
            if(ret['valuenum'] is not None):
                centimeters = float(ret['valuenum'])
                centimeters *= 2.54
                centimeters = str(centimeters)

            else:
               centimeters = -1
            f.write("00:00,Height,{0}\n".format(centimeters))


##        # Access Patient's ICU Type.
##        sql = "SELECT first_careunit \
##               FROM mimiciii.icustays \
##               WHERE subject_id = (%s) AND hadm_id = {};".format(last_hadm_id)
##        cur.execute(sql,(subject_id,))
##        ret = cur.fetchall()
##        if cur.rowcount is 0:
##            icutype = -1
##        else:
##            icutype = ret[-1]
##            if icutype is None:
##                icutype = -1
##            else:
##                icutype = icutype[0]
##                if (icutype == "CCU"):
##                    icutype = 1
##                elif (icutype == "CSRU"):
##                    icutype = 2
##                elif (icutype == "MICU"):
##                    icutype = 3
##                elif (icutype == "SICU"):
##                    icutype = 4
##                else: icutype = -1
        
        f.write("00:00,ICUType,{0}\n".format(icutype))

        #Patient weight
        sql = "SELECT chartevents.valuenum \
                FROM mimiciii.chartevents \
                WHERE chartevents.itemid IN(762, 763, 3723, 3580) \
                AND chartevents.subject_id = {0} \
                AND chartevents.valuenum IS NOT NULL \
                LIMIT 1;".format(subject_id)
        cur.execute(sql)

        if (cur.rowcount == 0):
            value = -1
        else:
            ret = cur.fetchone()
            if (ret['valuenum'] is None):
                value = -1
            else:
                value = ret['valuenum']
            
        f.write("00:00,Weight,{0}\n".format(str(value)))

        #mechanical ventilation
        sql = "SELECT mechvent from ventfirstday where subject_id = {} \
        and hadm_id = {};".format(subject_id, last_hadm_id)
        cur.execute(sql)
        if (cur.rowcount is not 0):
            ret = cur.fetchone()
            if(ret['mechvent'] is not None):
               value = ret['mechvent']
               if(int(value) is 1):
                   if(verbose): print("mechvent is 1")
                   f.write("00:00,MechVent,1\n")
        
 
        #print("initial time = ", initialTime)
        #construct string to enter in file
        for row in result:
            ##Conversions
            #MechVent
            if(row['itemid'] == 722): row['valuenum'] = 1

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
                #print("Could not add: {}\n".format(s))
            #Ignore empty measurements
            elif(str(row['valuenum']) != ""):
                if(row['itemid'] in URINEIDS):
                   s = str(outputTime) + "," + "Urine" + "," + str(row['valuenum']) + "\n"
                else: s = str(outputTime) + "," + str(label(str(row['itemid']))) + "," + str(row['valuenum']) + "\n"
                f.write(s)
        count +=1
        if ((count % 500) is 0):
            print("Processed {} records out of {}...".format(count, num_subjects))
    f.close()

print("Done.")
print("Results: {} subject files created, {} subjects skipped.".format(count, original_subjects-num_subjects))
os.chdir("..")


conn.close()







