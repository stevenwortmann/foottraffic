CREATE OR ALTER PROCEDURE [dbo].[insertVisitsType_Work](
	@a_placekey VARCHAR(max),
	@ac_poicbg BIGINT,
	@w_daterangestart VARCHAR(max),
	@af_visitordaytimecbg BIGINT,
	@af_visitordaytimecbg_cnt INT
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @cbgidout INT;
DECLARE @locidout INT;

BEGIN

  SET @locidout=(SELECT locid FROM locationInfo WHERE placekey=@a_placekey) 

  IF (SELECT COUNT(1) FROM censusBlockGroups WHERE cbg_number=@af_visitordaytimecbg)=1
    BEGIN
      SET @cbgidout=(SELECT cbgid FROM censusBlockGroups WHERE cbg_number=@af_visitordaytimecbg);
    END;

  ELSE
    BEGIN
      INSERT INTO censusBlockGroups(cbg_number)
      VALUES (@af_visitordaytimecbg);
      SET @cbgidout=(SELECT TOP 1 cbgid FROM censusBlockGroups ORDER BY cbgid DESC);
    END;

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
		    SET @vidout = (SELECT TOP 1 vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart) ORDER BY vid DESC);	
        INSERT INTO visitsType(locid, vid, cbgid_loc, cbgid_orig, visit_count, home_work_ind)
        VALUES (@locidout, @vidout, @ac_poicbg, @cbgidout, @af_visitordaytimecbg_cnt, 'w');
    END;
END;
END;