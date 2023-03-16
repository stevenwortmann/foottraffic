CREATE OR ALTER PROCEDURE [dbo].[insertVisitsType_Home](
  @a_placekey VARCHAR(max),
	@ac_poicbg BIGINT,
  @w_daterangestart VARCHAR(max),
  @ad_visitorhomecbg VARCHAR(max),
  @ad_visitorhomecbg_cnt INT
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @cbgidout_loc INT;
DECLARE @cbgidout_orig INT;
DECLARE @locidout INT;

BEGIN

  SET @locidout=(SELECT locid FROM locationInfo WHERE placekey=@a_placekey)
  SET @cbgidout_loc=(SELECT cbgid FROM censusBlockGroups WHERE cbg_number=@ac_poicbg)

  IF (SELECT COUNT(1) FROM censusBlockGroups WHERE cbg_number=@ad_visitorhomecbg)=1
    BEGIN
      SET @cbgidout_orig=(SELECT cbgid FROM censusBlockGroups WHERE cbg_number=@ad_visitorhomecbg);
    END;

  ELSE
    BEGIN
      INSERT INTO censusBlockGroups(cbg_number)
      VALUES (@ad_visitorhomecbg);
      SET @cbgidout_orig=(SELECT TOP 1 cbgid FROM censusBlockGroups ORDER BY cbgid DESC);
    END;

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
		    SET @vidout = (SELECT TOP 1 vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart) ORDER BY vid DESC);	
        INSERT INTO visitsType(locid, vid, cbgid_loc, cbgid_orig, visit_count, home_work_ind)
        VALUES (@locidout, @vidout, @cbgidout_loc, @cbgidout_orig, @ad_visitorhomecbg_cnt, 'h');
    END;
END;
END;