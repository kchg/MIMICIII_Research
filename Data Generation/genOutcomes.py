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
icustays = []
try:
    for filename in sorted(os.listdir(os.getcwd())):
        icustays.append(int(filename.strip('.txt')))
except:
    print ("Could not iterate through files")
    sys.exit()
numfiles = len([name for name in os.listdir('.') if os.path.isfile(name)])
os.chdir("..")

icustays.sort()

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
    for icustay_id in icustays:
        default = "{}, -1, -1, -1, -1, -1\n".format(icustay_id)
        if((count % 500) is 0):
            print("Generated {} of {} outcomes...".format(count, numfiles))
        count = count+1
        saps = -1

        cur.execute(open('genDataScripts/outcomes.sql','r').read().format(icustay_id))
        data = cur.fetchone()
        if data is None:
            f.write(default)
            print("had to default for {}".format(icustay_id))
            continue

        ihd = data['ihd']
        if ihd is 1:
            survival = (data['dod'] - data['intime']).days
        else: survival = -1

        #write
        f.write("{},{},{},{},{},{}\n".format(icustay_id, data['saps'], data['sofa'], int(data['los']), survival, ihd))
    f.close()
    print("Done.")
conn.close()
