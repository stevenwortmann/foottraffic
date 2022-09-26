ALTER PROCEDURE insertBrandsWeek(
	@a_placekey VARCHAR(max),
	@w_daterangestart VARCHAR(max),
	@al_relatedsameweekbrand VARCHAR(max),
	@al_relatedsameweekbrand_cnt INT
)
AS
BEGIN
DECLARE @vidout INT;
DECLARE @bidout INT;
DECLARE @locidout INT;

BEGIN

	IF (SELECT COUNT(1) FROM brandsInfo WHERE brand_name=@al_relatedsameweekbrand)=1
		BEGIN
			SET @bidout=(SELECT bid FROM brandsInfo WHERE brand_name=@al_relatedsameweekbrand);
		END;
	ELSE
		BEGIN
			INSERT INTO brandsInfo(brand_name)
			VALUES (@al_relatedsameweekbrand);
			SET @bidout=(SELECT TOP 1 bid FROM brandsInfo ORDER BY bid DESC);
		END;


	IF (SELECT COUNT(1) FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart))=1 
	BEGIN
		SET @vidout = (SELECT TOP 1 vid FROM visitsInfo v JOIN locationInfo l ON v.locid=l.locid WHERE (l.placekey=@a_placekey AND v.week_begin=@w_daterangestart) ORDER BY vid DESC);
		SET @locidout = (SELECT locid FROM locationInfo l WHERE l.placekey=@a_placekey);		
		INSERT INTO brandsWeek(vid, bid, locid, visit_count)
		VALUES (@vidout, @bidout, @locidout, @al_relatedsameweekbrand_cnt);
	END;
END;
END;