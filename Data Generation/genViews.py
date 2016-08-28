#/user/bin/python3.4

#This program generates materialized views for a mimic database to
#calculate SAPS, SOFA, and various other severity scores.
import psycopg2
import psycopg2.extras
import os
import shutil
import time
import re
import sys
from genHelper import connect

#connect to MIMIC
conn = connect()

os.chdir("severityscores")
os.chdir("requiredviews")
cursor = conn.cursor()
#run the sql files
print("Starting: this process took ~40 minutes to run on my machine")
for filename in sorted(os.listdir(os.getcwd())): 
    print ("Creating materialized view {}...".format(str(filename)))
    cursor.execute(open(filename, "r").read())

os.chdir("..")
print ("Generating SAPS...")
cursor.execute(open("saps.sql", "r").read())
print ("Generating SOFA...")
cursor.execute(open("sofa.sql", "r").read())

