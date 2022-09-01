CREATE PROCEDURE insertBrandsWeek(
	@a_placekey VARCHAR(max),
	@w_daterangestart VARCHAR(max),
	@al_relatedsameweekbrand VARCHAR(max),
	@al_relatedsameweekbrand_cnt INT
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @bidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
        SELECT @vidout = LAST_VALUE(vid) OVER (ORDER BY vid) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart);
		SELECT @bidout = LAST_VALUE(bid) OVER (ORDER BY bid) FROM brandsInfo WHERE (brand_name=@al_relatedsameweekbrand);
        INSERT INTO brandsWeek(vid, bid, visit_count)
        VALUES (@vidout, @bidout, @al_relatedsameweekbrand_cnt);
    END;
END;
END;