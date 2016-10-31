with t1 as
(
  select
    ie.subject_id, ie.hadm_id, ie.icustay_id,
	CASE
	WHEN gender = 'F'
	THEN '0'
	WHEN gender = 'M'
	THEN '1'
	ELSE '-1'
	END AS gender_num,
	CASE
	WHEN first_careunit = 'CCU'
	THEN '1'
	WHEN first_careunit = 'CSRU'
	THEN '2'
	WHEN first_careunit = 'MICU'
	THEN '3'
	WHEN first_careunit = 'SICU'
	THEN '4'
	ELSE '-1'
	END AS icutype
    , ie.intime, ie.outtime
    , ROW_NUMBER() over (PARTITION BY ie.subject_id ORDER BY ie.intime) as rn
    , pt.dob
  from mimiciii.icustays ie
  -- filter down to only adult patients
  inner join mimiciii.patients pt
    on ie.subject_id = pt.subject_id
    and pt.dob < (ie.intime - interval '16' year)
)
, t2 as
(
  select
    *, extract('year' from age(intime,dob)) as age
  from t1
  -- filter to only the FIRST ICU stay
  where rn = 1
  -- also filter to only stays >= 48 hours
  and (outtime-intime) >= interval '48' hour
)
, t3 as
(
select t2.*, heightweight.height_first, heightweight.weight_first
from t2
left join mimiciii.heightweight on t2.icustay_id = heightweight.icustay_id
)

select
t3.*, vfd.mechvent
from t3 left join ventfirstday vfd on t3.icustay_id = vfd.icustay_id
order by t3.icustay_id;


