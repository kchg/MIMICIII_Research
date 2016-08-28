SELECT
  d_labitems.label AS Item,  
  d_labitems.itemid AS ItemID

FROM 
  mimiciii.d_labitems
WHERE UPPER(d_labitems.label) LIKE UPPER('%%')

;

