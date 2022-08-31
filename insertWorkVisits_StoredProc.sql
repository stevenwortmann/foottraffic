CREATE PROCEDURE insertWorkVisits(
  a_placekey VARCHAR(max),
  w_daterangestart VARCHAR(max),
  af_visitordaytimecbg VARCHAR(max),
  af_visitordaytimecbg_cnt INT,
)
AS $$
DECLARE @vidout INT;
DECLARE @cbgidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo WHERE (placekey=a_placekey AND week_begin=w_daterangestart))=1 
    BEGIN
        SELECT vid INTO @vidout FROM visitsInfo WHERE (placekey=a_placekey AND week_begin=w_daterangestart)
        SELECT cbgid INTO @cbgidout FROM censusBlockGroups WHERE (cbg_number=af_visitordaytimecbg)
        INSERT INTO homeVisits(vid, cbgid, visit_count)
        VALUES (@vidout, @cbgidout, af_visitordaytimecbg_cnt);
    END IF;
END;