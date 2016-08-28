SELECT 
  patients.subject_id
FROM 
  mimiciii.patients
ORDER BY RANDOM()
LIMIT 4000;
