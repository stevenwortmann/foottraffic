CREATE PROCEDURE insertWorkVisits(
	@a_placekey VARCHAR(max),
	@w_daterangestart VARCHAR(max),
	@af_visitordaytimecbg VARCHAR(max),
	@af_visitordaytimecbg_cnt INT,
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @cbgidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
		SELECT @vidout = LAST_VALUE(vid) OVER (ORDER BY vid) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart);
		SELECT @cbgidout = LAST_VALUE(cbgid) OVER (ORDER BY cbgid) FROM censusBlockGroups WHERE (cbg_number=@af_visitordaytimecbg);
        INSERT INTO homeVisits(vid, cbgid, visit_count)
        VALUES (@vidout, @cbgidout, @af_visitordaytimecbg_cnt);
    END;
END;