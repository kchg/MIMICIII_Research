SELECT
  labevents.itemid,
  labevents.value,
  'Lab Event' AS Type 
FROM 
  mimiciii.labevents
WHERE mimiciii.labevents.itemid = 212
LIMIT 100;

