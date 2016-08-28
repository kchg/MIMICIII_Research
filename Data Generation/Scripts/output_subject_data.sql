SELECT 
  chartevents.subject_id, 
  chartevents.itemid, 
  chartevents.charttime, 
  chartevents.value,
  d_items.label
  
FROM 
  mimiciii.chartevents
	LEFT JOIN mimiciii.d_items
		ON mimiciii.chartevents.itemid = mimiciii.d_items.itemid

WHERE subject_id = 423


UNION ALL

SELECT
  labevents.subject_id,
  labevents.itemid,
  labevents.charttime,
  labevents.value,
  d_labitems.label


FROM
  mimiciii.labevents
	LEFT JOIN mimiciii.d_labitems
		ON mimiciii.labevents.itemid = mimiciii.d_labitems.itemid

WHERE subject_id = 423
ORDER BY charttime
;

