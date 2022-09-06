ALTER PROCEDURE insertHomeVisits(
  @a_placekey VARCHAR(max),
  @w_daterangestart VARCHAR(max),
  @ad_visitorhomecbg VARCHAR(max),
  @ad_visitorhomecbg_cnt INT
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @cbgidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
      SET @vidout = (SELECT TOP 1 vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart) ORDER BY vid DESC);	
		  SET @cbgidout=(SELECT TOP 1 cbgid FROM censusBlockGroups  WHERE (cbg_number=@ad_visitorhomecbg) ORDER BY cbgid DESC);
        INSERT INTO homeVisits(vid, cbgid, visit_count)
        VALUES (@vidout, @cbgidout, @ad_visitorhomecbg_cnt);
    END;
END;
END;