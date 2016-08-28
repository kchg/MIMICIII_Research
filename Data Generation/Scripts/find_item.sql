SELECT DISTINCT
  d_labitems.label,  
  d_labitems.itemid,
  'Lab Item' AS Type 
FROM 
  mimiciii.d_labitems
WHERE UPPER(d_labitems.label) LIKE UPPER('%bp%')

UNION ALL

SELECT DISTINCT
  d_items.label as abc,
  d_items.itemid as bcd,
  'Item' AS Type
FROM
  mimiciii.d_items
WHERE
  UPPER(d_items.label) LIKE UPPER('%bp%');
