SELECT
  d_items.label AS Item,  
  d_items.itemid AS ItemID



FROM 
  mimiciii.d_items

WHERE UPPER(d_items.label) LIKE UPPER('%%')

;

