from datetime import datetime
from dateutil.relativedelta import relativedelta
import sys
import psycopg2
import psycopg2.extras
import os
import shutil
import time

#connect to mimic database
def connect():
    params = {
        'database': 'mimic',
        'user': 'mimic',
        'password': 'mimic',
        'host': 'localhost',
        'port': 5432
    }
    try:
        print ("Connecting to {}...".format(params['host']))
        conn=psycopg2.connect(**params)
    except:
        print ("Unable to connect to database. Exiting.")
        sys.exit()
    return conn

print ("Connected")
# Function to return the age of the patient.
def getAge(ICUdate, birthdate):
    return relativedelta(ICUdate, birthdate).years

def label(x):
    return items.get(x, 0)

def translateGender(g):
    if(g == "M"): return 0
    else: return 1

items = {
    '50862':'Albumin', '227456':'Albumin','3066':'Albumin','1521':'Albumin','226981':'Albumin',
    '50863':'ALP','3728':'ALP',
    '50861':'ALT','769':'ALT','220644':'ALT',
    '50878':'AST','220587':'AST',
    '50885':'Bilirubin','225690':'Bilirubin',
    '51006':'BUN','1162':'BUN','225624':'BUN',
    '50907':'Cholesterol','789':'Cholesterol','1524':'Cholesterol','220603':'Cholesterol','3748':'Cholesterol',
    '50912':'Creatinine','51081':'Creatinine','227005':'Creatinine','1525':'Creatinine','220615':'Creatinine',
    '225310':'DiasABP','8368':'DiasABP','220051':'DiasABP','8555':'DiasABP','8364':'DiasABP',
    '223835':'FiO2','3420':'FiO2',
    '198':'GCS','226755':'GCS',
    '50809':'Glucose','50931':'Glucose','227015':'Glucose','3744':'Glucose','1529':'Glucose',
    '227443':'HCO3','226759':'HCO3','812':'HCO3',
    '51480':'HCT','51221':'HCT','227017':'HCT','813':'HCT',
    '220045':'HR','211':'HR',
    '50971':'K','227442':'K','1535':'K',
    '50813':'Lactate','1531':'Lactate','225668':'Lactate',
    '50960':'Mg','1532':'Mg','220635':'Mg',
    '224':'MAP','224322':'MAP',
    '722':'MechVent',
    '50983':'Na','1536':'Na','220645':'Na',
    '220180':'NIDiasABP','8441':'NIDiasABP',
    '220052':'NIMAP','220181':'NIMAP',
    '220179':'NISysABP','455':'NISysABP',
    '778':'PaCO2',
    '779':'PaO2',
    '780':'pH','50831':'pH','50820':'pH','223830':'pH',
    '51265':'Platelets','828':'Platelets','227457':'Platelets',
    '618':'RespRate','3603':'RespRate','220210':'RespRate',
    '50817':'SaO2','220227':'SaO2',
    '225309':'SysABP','51':'SysABP','220050':'SysABP',
    '50825':'Temp','3655':'Temp','677':'Temp','223762':'Temp','676':'Temp',
    '51002':'TroponinI',
    '51003':'TroponinT','227429':'TroponinT',	
    #'51108':'Urine',
    '51301':'WBC','51300':'WBC','220546':'WBC','1542':'WBC',
    '762':'Weight','3723':'Weight','763':'Weight','3580':'Weight'
}

URINEIDS = (40055,43175,40069,40094,40715,40473,40085,40057,40056,40405,40428,40086,40096,40651,226559,226560,227510,226561,226584,226563,226564,226565,226567,226557,226558)

ITEM_QUERY = "\
SELECT \
 chartevents.charttime, chartevents.itemid, chartevents.valuenum, d_items.label \
FROM \
  mimiciii.chartevents \
	LEFT JOIN mimiciii.d_items \
		ON mimiciii.chartevents.itemid = mimiciii.d_items.itemid \
\
WHERE subject_id = (%s) \
AND chartevents.itemid = ANY(%s) \
\
UNION ALL \
\
SELECT \
  labevents.charttime, \
  labevents.itemid,\
  labevents.valuenum, \
  d_labitems.label \
\
FROM \
  mimiciii.labevents \
	LEFT JOIN mimiciii.d_labitems \
		ON mimiciii.labevents.itemid = mimiciii.d_labitems.itemid \
\
WHERE subject_id = (%s) \
AND labevents.itemid = ANY(%s) \
\
UNION ALL \
\
select charttime, itemid, value as valuenum, NULL as label \
from mimiciii.outputevents \
where itemid in(40055,43175,40069,40094,40715,40473,40085,40057,40056,40405,40428,40086,40096,40651,226559,226560,227510,226561,226584,226563,226564,226565,226567,226557,226558) \
and upper(valueuom) like upper('ML') \
and valueuom not like '' \
and subject_id = (%s) \
ORDER BY charttime;"

ITEM_QUERY_CUSTOM_DATE = "\
SELECT \
 chartevents.charttime, chartevents.itemid, chartevents.valuenum, d_items.label \
FROM \
  mimiciii.chartevents \
	LEFT JOIN mimiciii.d_items \
		ON mimiciii.chartevents.itemid = mimiciii.d_items.itemid \
\
WHERE subject_id = (%s) AND chartevents.hadm_id = (%s) \
AND chartevents.itemid = ANY(%s) \
\
UNION ALL \
\
SELECT \
  labevents.charttime, \
  labevents.itemid,\
  labevents.valuenum, \
  d_labitems.label \
\
FROM \
  mimiciii.labevents \
	LEFT JOIN mimiciii.d_labitems \
		ON mimiciii.labevents.itemid = mimiciii.d_labitems.itemid \
\
WHERE subject_id = (%s) AND labevents.hadm_id = (%s) \
AND labevents.itemid = ANY(%s) \
\
UNION ALL \
\
select charttime, itemid, value as valuenum, NULL as label  \
from mimiciii.outputevents \
where itemid in(40055,43175,40069,40094,40715,40473,40085,40057,40056,40405,40428,40086,40096,40651,226559,226560,227510,226561,226584,226563,226564,226565,226567,226557,226558) \
and upper(valueuom) like upper('ML') \
and valueuom not like '' \
and subject_id = (%s) AND hadm_id = (%s) \
ORDER BY charttime;"
    
