with icudetails as (select icustay_id, subject_id, intime, outtime
from mimiciii.icustays where icustay_id = {0}),

icuvalues as (
select subject_id, itemid, charttime, valuenum from mimiciii.labevents 
where subject_id = (select distinct subject_id from icudetails)
and charttime < (select outtime from icudetails)
and charttime > (select intime from icudetails)
and valuenum is not null

UNION ALL

select subject_id, itemid, charttime, valuenum from mimiciii.chartevents
where icustay_id = {0}
)
select charttime, itemid, valuenum from icuvalues
where itemid = ANY(%s)

UNION ALL

select charttime, itemid, value as valuenum
from mimiciii.outputevents 
where itemid = ANY(%s)
and upper(valueuom) like upper('ML') 
and valueuom not like '' 
and icustay_id = {0}

order by charttime
;

