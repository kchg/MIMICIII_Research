import psycopg2
import psycopg2.extras
import os
import shutil
import time
import re
import sys
from genHelper import *
from datetime import timedelta

#connect to MIMIC
conn = connect()

#define dictionary cursor to work with (keyed on column name)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) #results in dictionary form

#retrieve subject ids to caculate outcomes for
os.chdir("set-a")
subjects = []
try:
    for filename in sorted(os.listdir(os.getcwd())):
        subjects.append(int(filename.strip('.txt')))
except:
    print ("Could not iterate through files")
    sys.exit()
numfiles = len([name for name in os.listdir('.') if os.path.isfile(name)])
os.chdir("..")

subjects.sort()

print("Generating Outcomes...")
#file management
filename = "Outcomes-a.txt"
#delete if exists
try:
    os.remove(filename)
except OSError:
    pass

with open(filename, "w") as f:
    count = 0
    f.write("RecordID, SAPS-I, SOFA, Length_of_stay, Survival, In-hospital_death\n")
    for subject_id in subjects:
        default = "{}, -1, -1, -1, -1, -1\n".format(subject_id)
        if((count % 500) is 0):
            print("Generated {} of {} outcomes...".format(count, numfiles))
        count = count+1
        saps = -1

        #####################################
        #have only last icustay
        numhadmquery = "select subject_id, hadm_id, admittime, deathtime \
           from mimiciii.admissions where subject_id = {} order by admittime;".format(subject_id)
        cur.execute(numhadmquery)
        hadm_ids = cur.fetchall()
        if(len(hadm_ids) is 0):
            f.write(default)
            continue
        last_id = hadm_ids[-1]
        last_hadm_id = last_id['hadm_id']

        #saps score
        SAPS_QUERY = "SELECT saps FROM saps WHERE subject_id = {} AND hadm_id = {}".format(subject_id, last_hadm_id)
        cur.execute(SAPS_QUERY)
        if(cur.rowcount == 0): saps = -1
        else:
            saps = cur.fetchone()
            saps = saps[0]
            
        #sofa score
        SOFA_QUERY = "SELECT sofa FROM sofa WHERE subject_id = {}".format(subject_id)
        cur.execute(SOFA_QUERY)
        if(cur.rowcount == 0): sofa = -1
        else:
            sofa = cur.fetchone()
            sofa = sofa[0]






        #in hospital death
        sql = "SELECT deathtime \
                FROM mimiciii.admissions \
                WHERE subject_id = {} AND hadm_id = {};".format(subject_id, last_hadm_id)
        cur.execute(sql)
        death_date = cur.fetchone()
        death_date = death_date[0]

        if(death_date is None):
            ihd = 0
        else:
            ihd = 1

        ADMISSION_DATE_QUERY = "SELECT admittime \
                                    FROM mimiciii.admissions \
                                    WHERE subject_id = {} \
                                    AND hadm_id = {};".format(subject_id, last_hadm_id)
        cur.execute(ADMISSION_DATE_QUERY)
        admit_date = cur.fetchone()
        if(cur.rowcount == 0): admit_date = -1
        else: admit_date = admit_date['admittime']
        #if in hospital death, calculate days between ICU admission and death
        if((str(ihd) is "1") and admit_date is not -1):
            survival = (death_date - admit_date).days
        else: survival = -1

        #length of stay for final admission
        OUT_DATE_QUERY = "SELECT dischtime \
                            FROM mimiciii.admissions \
                            WHERE subject_id = {} \
                            AND hadm_id = {};".format(subject_id, last_hadm_id)
        cur.execute(OUT_DATE_QUERY)
        
        out_date = cur.fetchone()
        if(cur.rowcount is 0): out_date = -1
        else: out_date = out_date['dischtime']
        if (out_date is None or admit_date is None or admit_date is -1 or out_date is -1):
            stay = -1
        else:
            stay = (out_date - admit_date).days

        #write
        f.write("{},{},{},{},{},{}\n".format(subject_id, saps, sofa, stay, survival, ihd))
    f.close()
    print("Done.")
conn.close()
