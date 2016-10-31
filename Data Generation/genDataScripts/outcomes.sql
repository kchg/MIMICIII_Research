with 

icuinfo as (
select icustays.icustay_id, icustays.los, icustays.intime, icustays.outtime, icustays.subject_id, saps.saps
from mimiciii.icustays left join saps on saps.icustay_id = icustays.icustay_id
where icustays.icustay_id = {}
),

t1 as (
select icuinfo.*, sofa.sofa from icuinfo 
left join sofa on icuinfo.icustay_id = sofa.icustay_id
)

select t1.*, patients.dod,
CASE
WHEN patients.dod < t1.outtime
THEN 1
ELSE 0
END AS ihd
from t1 left join mimiciii.patients on t1.subject_id = patients.subject_id