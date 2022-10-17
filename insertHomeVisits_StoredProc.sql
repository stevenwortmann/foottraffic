ALTER PROCEDURE [dbo].[insertHomeVisits](
  @a_placekey VARCHAR(max),
  @w_daterangestart VARCHAR(max),
  @ad_visitorhomecbg VARCHAR(max),
  @ad_visitorhomecbg_cnt INT
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @cbgidout INT;
DECLARE @locidout INT;

BEGIN

  SET @locidout=(SELECT locid FROM locationInfo WHERE placekey=@a_placekey) 

  IF (SELECT COUNT(1) FROM censusBlockGroups WHERE cbg_number=@ad_visitorhomecbg)=1
    BEGIN
      SET @cbgidout=(SELECT cbgid FROM censusBlockGroups WHERE cbg_number=@ad_visitorhomecbg);
    END;

  ELSE
    BEGIN
      INSERT INTO censusBlockGroups(cbg_number)
      VALUES (@ad_visitorhomecbg);
      SET @cbgidout=(SELECT TOP 1 cbgid FROM censusBlockGroups ORDER BY cbgid DESC);
    END;

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
        SET @vidout = (SELECT TOP 1 vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart) ORDER BY vid DESC);	
        INSERT INTO homeVisits(locid, vid, cbgid, visit_count)
        VALUES (@locidout, @vidout, @cbgidout, @ad_visitorhomecbg_cnt);
    END;
END;
END;