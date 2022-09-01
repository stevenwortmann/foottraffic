CREATE PROCEDURE insertBrandsDay(
	@a_placekey VARCHAR(max),
	@w_daterangestart VARCHAR(max),
	@ak_relatedsamedaybrand VARCHAR(max),
	@ak_relatedsamedaybrand_cnt INT,
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @bidout INT;

BEGIN

  IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
    BEGIN
        SELECT @vidout = LAST_VALUE(vid) OVER (ORDER BY vid) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart);
		SELECT @bidout = LAST_VALUE(bid) OVER (ORDER BY bid) FROM brandsInfo WHERE (brand_name=@ak_relatedsamedaybrand);
        INSERT INTO brandsDay(vid, bid, visit_count)
        VALUES (@vidout, @bidout, @ak_relatedsamedaybrand_cnt);
    END;
END;