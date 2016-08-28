To get access to the MIMIC-III database, request access from http://mimic.physionet.org/gettingstarted/access/ and setup the server according to the tutorials section of the website.

To run these programs on your machine, download psycopg for python at http://initd.org/psycopg/.

****Generate Data*****
1) Edit params in genHelper.py to log in to your database.
2) Run genViews.py to create the materialized views to help generate the tables
	required to generate the severity scores in the outcomes file. This process
	takes a while (about an hour).
3) Run genData.py. This will create a folder called "set-a" and place each patient
	entry's data in its own text file, with the filename as the subject_id. This
	program takes about an hour to run on ~40000 patients.
4) Run genOutcomes.py, which will create a file called "Outcomes-a.txt" that
	contains subject_id, SAPS score, SOFA score, length of stay, survival, and 
	in-hospital death. This program takes about half an hour to run on ~40000 entries.
	
Optional:
outcomesStats.py tells you the number of patients and how many of them died
in the hospital.