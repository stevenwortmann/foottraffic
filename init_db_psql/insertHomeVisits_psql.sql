CREATE OR REPLACE PROCEDURE insertHomeVisits(
  a_placekey VARCHAR,
  w_daterangestart DATE,
  ad_visitorhomecbg VARCHAR,
  ad_visitorhomecbg_cnt INT
)
AS $$
DECLARE vidout INT;
DECLARE cbgidout INT;
DECLARE locidout INT;
BEGIN
  SELECT locid INTO locidout FROM locationInfo WHERE placekey=a_placekey;

  IF EXISTS (SELECT 1 FROM censusBlockGroups WHERE cbg_number=ad_visitorhomecbg) THEN
    SELECT cbgid INTO cbgidout FROM censusBlockGroups WHERE cbg_number=ad_visitorhomecbg;
  ELSE
    INSERT INTO censusBlockGroups(cbg_number)
        VALUES (ad_visitorhomecbg);
    SELECT LASTVAL() INTO cbgidout;
  END IF;

  IF EXISTS (SELECT 1 FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=a_placekey AND v.week_begin=w_daterangestart)) THEN
    SELECT vid INTO vidout FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=a_placekey AND v.week_begin=w_daterangestart);
    INSERT INTO visitsType(locid, vid, cbgid, visit_count, home_work_ind)
        VALUES (locidout, vidout, cbgidout, ad_visitorhomecbg_cnt, 'h');
  END IF;
END;