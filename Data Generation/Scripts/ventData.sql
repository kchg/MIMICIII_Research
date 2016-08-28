select count(*) from (select subject_id, icustay_id, itemid, charttime, hadm_id, value,
    -- case statement determining whether it is an instance of mech vent
      case
        when itemid = 720 and value != 'Other/Remarks' THEN 1  -- VentTypeRecorded
        when itemid = 467 and value = 'Ventilator' THEN 1 -- O2 delivery device == ventilator
        when itemid = 648 and value = 'Intubated/trach' THEN 1 -- Speech = intubated
        when itemid in (445, 448, 449, 450, 1340, 1486, 1600, 224687 -- minute volume
          , 639, 654, 681, 682, 683, 684,224685,224684,224686 -- tidal volume
          , 218,436,535,444,459,224697,224695,224696,224746,224747 -- High/Low/Peak/Mean/Neg insp force ("RespPressure")
          , 221,1,1211,1655,2000,226873,224738,224419,224750,227187 -- Insp pressure
          , 543 -- PlateauPressure
          , 5865,5866,224707,224709,224705,224706 -- APRV pressure
          , 60,437,505,506,686,220339,224700 -- PEEP
          , 3459 -- high pressure relief
          , 501,502,503,224702 -- PCV
          , 223,667,668,669,670,671,672 -- TCPCV
          , 157,158,1852,3398,3399,3400,3401,3402,3403,3404,8382,227809,227810 -- ETT
          , 224701 -- PSVlevel
	)
	then 1
       end as entries

     from mimiciii.chartevents ce 
	where itemid in(720,467,648,
	445, 448, 449, 450, 1340, 1486, 1600, 224687 -- minute volume
          , 639, 654, 681, 682, 683, 684,224685,224684,224686 -- tidal volume
          , 218,436,535,444,459,224697,224695,224696,224746,224747 -- High/Low/Peak/Mean/Neg insp force ("RespPressure")
          , 221,1,1211,1655,2000,226873,224738,224419,224750,227187 -- Insp pressure
          , 543 -- PlateauPressure
          , 5865,5866,224707,224709,224705,224706 -- APRV pressure
          , 60,437,505,506,686,220339,224700 -- PEEP
          , 3459 -- high pressure relief
          , 501,502,503,224702 -- PCV
          , 223,667,668,669,670,671,672 -- TCPCV
          , 157,158,1852,3398,3399,3400,3401,3402,3403,3404,8382,227809,227810 -- ETT
          , 224701 -- PSVlevel
          )
          AND value is not null
          )a
          where entries = 1