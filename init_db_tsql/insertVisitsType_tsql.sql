CREATE OR ALTER PROCEDURE [dbo].[insertVisitsType](
  @a_placekey VARCHAR(max),
  @w_daterangestart VARCHAR(max),
  @ad_af_visitorcbg VARCHAR(max),
  @ad_af_visitorcbg_cnt INT,
  home_work_ind CHAR(1)
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @cbgidout INT;
DECLARE @locidout INT;

BEGIN

  SET @locidout=(SELECT locid FROM locationInfo WHERE placekey=@a_placekey) 

  IF (SELECT COUNT(1) FROM censusBlockGroups WHERE cbg_number=@ad_af_visitorcbg)=1
    BEGIN
      SET @cbgidout=(SELECT cbgid FROM censusBlockGroups WHERE cbg_number=@ad_af_visitorcbg);
    END;

  ELSE
    BEGIN
      INSERT INTO censusBlockGroups(cbg_number)
      VALUES (@ad_af_visitorcbg);
      SET @cbgidout=(SELECT TOP 1 cbgid FROM censusBlockGroups ORDER BY cbgid DESC);
    END;

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
		    SET @vidout = (SELECT TOP 1 vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart) ORDER BY vid DESC);	
        INSERT INTO visitsType(locid, vid, cbgid, visit_count, home_work_ind)
        VALUES (@locidout, @vidout, @cbgidout, @ad_af_visitorcbg_cnt, home_work_ind);
    END;
END;
END;